// Inspect the actual GitHub-built HTML without contacting production services.
const { chromium } = require('playwright');
const fs = require('fs');
const {spawn} = require('child_process');
const path = require('path');
const output = process.env.COURSE_REVIEW_OUTPUT || '/tmp/course-browser-review';
fs.mkdirSync(output, {recursive:true});
// Serve the actual built artifact on loopback; no published account is used.
const server = spawn('python', ['-m','http.server','4174','--bind','127.0.0.1','--directory','_site'], {stdio:'ignore'});
process.on('exit', () => server.kill());
(async () => {
  for(let attempt=0; attempt<50; attempt++) {
    try { if((await fetch('http://127.0.0.1:4174/course/')).ok) break; } catch {}
    await new Promise(resolve=>setTimeout(resolve,100));
  }
  const browser = await chromium.launch({headless:true, args:['--no-sandbox']});
  const page = await browser.newPage();
  // Block analytics and all other external requests during isolated review.
  await page.route('**/*', route => route.request().url().startsWith('http://127.0.0.1:4174/') ? route.continue() : route.abort());
  const reports=[];
  const paths=['/course/','/course/m6/1/','/course/m7/2/','/course/m8/3/','/course/m9/3/','/course/m10/2/','/course/m11/1/','/course/m19/2/'];
  for(const width of [1280,360]) {
    await page.setViewportSize({width,height:900});
    for(const path of paths) {
      const response=await page.goto('http://127.0.0.1:4174'+path);
      if(response.status()!==200) throw new Error('Missing '+path);
      const detail=await page.evaluate(()=>({title:document.querySelector('h1')?.textContent.trim(), width:innerWidth, scrollWidth:document.documentElement.scrollWidth, citations:document.querySelectorAll('[id^="citation-"]').length, context:document.querySelector('.page-context')?.textContent.replace(/\s+/g,' ').trim()}));
      if(detail.scrollWidth>width+1) throw new Error('Horizontal page overflow: '+path+' '+JSON.stringify(detail));
      reports.push({path,width,...detail});
      if(path==='/course/m6/1/' || (width===360&&path==='/course/m9/3/')) {
        await page.screenshot({path:output+'/review-'+width+'-'+path.split('/').filter(Boolean).join('-')+'.png',fullPage:false});
      }
    }
  }
  await page.goto('http://127.0.0.1:4174/course/m7/2/');
  await page.locator('a[href="#for-clinicians-and-the-care-team"]').first().click();
  if(!page.url().endsWith('#for-clinicians-and-the-care-team')) throw new Error('Audience jump failed');
  // Check the final-head rendered anchors, not just Markdown source syntax.
  const broken=await page.evaluate(()=>Array.from(document.querySelectorAll('a[href^="#"]')).filter(a=>a.hash&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash));
  if(broken.length) throw new Error('Broken local anchors '+JSON.stringify(broken));
  fs.writeFileSync(output+'/report.json',JSON.stringify(reports,null,2));
  console.log('PASS: '+reports.length+' desktop/mobile rendered page checks; audience jump and local anchors.');
  await browser.close();
  server.kill();
})().catch(error=>{console.error(error.message);process.exit(1);});
