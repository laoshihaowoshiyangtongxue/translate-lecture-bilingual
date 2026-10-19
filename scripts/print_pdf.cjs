const {pathToFileURL}=require('url');
const path=require('path');
const args={};
for(let i=2;i<process.argv.length;i+=2) args[process.argv[i].replace(/^--/,'')]=process.argv[i+1];
for(const key of ['html','pdf','pages']) if(!args[key]) throw new Error('Missing --'+key);
if(!Number.isInteger(Number(args.pages))||Number(args.pages)<1) throw new Error('Invalid --pages');
(async()=>{
  const {chromium}=require(args.playwright ? path.resolve(args.playwright) : 'playwright');
  const browser=await chromium.launch({...(args.browser ? {executablePath:path.resolve(args.browser)} : {}),headless:true});
  try {
    const page=await browser.newPage({viewport:{width:1482,height:1016}});
    await page.goto(pathToFileURL(path.resolve(args.html)).href);
    await page.emulateMedia({media:'print'});
    await page.evaluate(()=>document.fonts.ready);
    const check=await page.evaluate(()=>({
      pages:document.querySelectorAll('section').length,
      brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
      overflow:[...document.querySelectorAll('section,article,math')].filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>e.closest('section')?.id),
      tooTall:[...document.querySelectorAll('section')].filter(e=>e.getBoundingClientRect().height>1016).map(e=>e.id),
      math:document.querySelectorAll('math').length
    }));
    console.log(JSON.stringify(check));
    if(check.pages!==Number(args.pages)||check.brokenImages||check.overflow.length||check.tooTall.length) throw new Error('Layout verification failed; inspect content and CSS before exporting.');
    await page.pdf({path:path.resolve(args.pdf),preferCSSPageSize:true,printBackground:true});
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
