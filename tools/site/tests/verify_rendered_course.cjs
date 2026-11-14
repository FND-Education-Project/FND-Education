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
  const paths=['/course/','/course/m6/1/','/course/m6/2/','/course/m6/3/','/course/m7/','/course/m7/1/','/course/m7/2/','/course/m7/3/','/course/m7/4/','/course/m7/5/','/course/m7/6/','/course/m8/','/course/m8/1/','/course/m8/2/','/course/m8/3/','/course/m9/','/course/m9/1/','/course/m9/2/','/course/m9/3/','/course/m10/','/course/m10/1/','/course/m10/2/','/course/m10/3/','/course/m11/1/','/course/m19/2/'];
  for(const width of [1280,360]) {
    await page.setViewportSize({width,height:900});
    for(const path of paths) {
      const response=await page.goto('http://127.0.0.1:4174'+path);
      if(response.status()!==200) throw new Error('Missing '+path);
      const detail=await page.evaluate(()=>({title:document.querySelector('h1')?.textContent.trim(), width:innerWidth, scrollWidth:document.documentElement.scrollWidth, citations:document.querySelectorAll('[id^="citation-"]').length, context:document.querySelector('.page-context')?.textContent.replace(/\s+/g,' ').trim()}));
      if(detail.scrollWidth>width+1) throw new Error('Horizontal page overflow: '+path+' '+JSON.stringify(detail));
      reports.push({path,width,...detail});
      // Audit reviewed Modules 6, 7, 8, 9 and 10 lessons at both widths using built HTML.
      // Local anchors and PDF affordances must survive Markdown conversion.
      if(/^\/course\/m(?:[6789]|10)\/\d+\/$/.test(path)) {
        const issues=await page.evaluate(()=>({
          anchors:Array.from(document.querySelectorAll('a[href^="#"]'))
            .filter(a=>a.hash&&!document.getElementById(decodeURIComponent(a.hash.slice(1))))
            .map(a=>a.hash),
          pdfs:Array.from(document.querySelectorAll('a[href$=".pdf"]'))
            .filter(a=>a.target!=='_blank'||!a.relList.contains('noopener'))
            .map(a=>a.getAttribute('href'))
        }));
        if(issues.anchors.length||issues.pdfs.length) {
          throw new Error('Lesson link regression: '+path+' '+JSON.stringify(issues));
        }
        // Scroll to load the illustration and capture its caption at each width.
        const figure=page.locator('figure.image-60center');
        await figure.scrollIntoViewIfNeeded();
        await page.waitForFunction(()=>{
          const img=document.querySelector('figure.image-60center img');
          return img&&img.complete&&img.naturalWidth>0&&img.alt.trim().length>0;
        });
        await figure.screenshot({path:output+'/figure-'+width+'-'+path.split('/').filter(Boolean).join('-')+'.png'});
        await page.evaluate(()=>scrollTo(0,0));
      }
      if(/^\/course\/m(?:[6789]|10)\/\d+\/$/.test(path) || (width===360&&path==='/course/m9/3/')) {
        await page.screenshot({path:output+'/review-'+width+'-'+path.split('/').filter(Boolean).join('-')+'.png',fullPage:false});
      }
    }
  }
  // Verify all Modules 7–10 puzzle selector, preview and download against the
  // built artifact. This catches catalog errors that a lesson-only check misses.
  const catalog = JSON.parse(fs.readFileSync('_site/assets/puzzles/catalog.json', 'utf8'));
  const modulePuzzles = catalog.items.filter(item => [7, 8, 9, 10].includes(item.module));
  // Assert each reviewed collection separately so missing entries cannot cancel out.
  for (const [module, count] of [[7, 13], [8, 7], [9, 7], [10, 7]]) {
    if (modulePuzzles.filter(item => item.module === module).length !== count) {
      throw new Error('Unexpected puzzle count for Module '+module);
    }
  }
  for(const width of [1280,360]) {
    await page.setViewportSize({width,height:900});
    for(const item of modulePuzzles) {
      const url = '/puzzles/?collection='+item.collection+'&puzzle='+item.id;
      await page.goto('http://127.0.0.1:4174'+url);
      await page.waitForFunction(() => {
        const root=document.getElementById('puzzle-browser');
        const image=document.getElementById('puzzle-preview');
        return root&&!root.hidden&&image&&image.complete&&image.naturalWidth>0;
      });
      const detail=await page.evaluate(() => ({
        module:document.getElementById('puzzle-module').value,
        lesson:document.getElementById('puzzle-lesson').value,
        course:document.getElementById('puzzle-course').getAttribute('href'),
        title:document.getElementById('puzzle-title').textContent,
        links:Array.from(document.querySelectorAll('#puzzle-downloads a')).map(a=>({
          href:a.getAttribute('href'),newTab:a.target==='_blank'&&a.relList.contains('noopener')
        })),
        overflow:document.documentElement.scrollWidth>innerWidth+1
      }));
      if(detail.module!==String(item.module)||detail.lesson!==item.id||detail.course!==item.course||
        !detail.title.includes(item.title)||detail.overflow||
        detail.links.length!==Object.keys(item.downloads).length||
        detail.links.some(link=>!link.newTab||!Object.values(item.downloads).includes(link.href))) {
        throw new Error('Puzzle regression: '+url+' '+JSON.stringify(detail));
      }
      for(const href of Object.values(item.downloads)) {
        const response=await page.request.get('http://127.0.0.1:4174'+href);
        if(response.status()!==200) throw new Error('Missing puzzle download: '+href);
      }
      reports.push({path:url,width,...detail});
      // Capture representative beginning/end selections for visual review.
      if(item.id==='lesson-18'||item.id==='lesson-23'||[8,9,10].includes(item.module)) {
        await page.screenshot({path:output+'/puzzle-'+width+'-'+item.collection+'-'+item.id+'.png',fullPage:true});
      }
    }
    // Check Module 10's approved lesson selection survives collection switching.
    await page.selectOption('#puzzle-module','10');
    await page.selectOption('#puzzle-lesson','lesson-31');
    await page.locator('[data-collection="crosswords"]').click();
    await page.locator('[data-collection="colouring"]').click();
    if(await page.locator('#puzzle-lesson').inputValue()!=='lesson-31') {
      throw new Error('Module 10 collection switch lost the selected lesson');
    }
    // Confirm Module 9 retains its lesson when switching collections.
    await page.selectOption('#puzzle-module','9');
    await page.selectOption('#puzzle-lesson','lesson-28');
    await page.locator('[data-collection="colouring"]').click();
    if(await page.locator('#puzzle-lesson').inputValue()!=='lesson-28') {
      throw new Error('Module 9 collection switch lost the selected lesson');
    }
    // Exercise Module 8's controls after all deep-link checks, including a
    // collection change that must preserve the selected lesson.
    await page.selectOption('#puzzle-module','8');
    await page.selectOption('#puzzle-lesson','lesson-25');
    await page.locator('[data-collection="colouring"]').click();
    if(await page.locator('#puzzle-lesson').inputValue()!=='lesson-25') {
      throw new Error('Module 8 collection switch lost the selected lesson');
    }
    // Exercise the selector controls rather than only restoring deep links.
    await page.selectOption('#puzzle-module','7');
    await page.selectOption('#puzzle-lesson','lesson-21');
    await page.locator('[data-collection="colouring"]').click();
    if(await page.locator('#puzzle-lesson').inputValue()!=='lesson-21') {
      throw new Error('Collection switch lost the selected lesson');
    }
  }
  await page.goto('http://127.0.0.1:4174/course/m7/2/');
  await page.locator('a[href="#for-clinicians-and-the-care-team"]').first().click();
  if(!page.url().endsWith('#for-clinicians-and-the-care-team')) throw new Error('Audience jump failed');
  // Check the final-head rendered anchors, not just Markdown source syntax.
  const broken=await page.evaluate(()=>Array.from(document.querySelectorAll('a[href^="#"]')).filter(a=>a.hash&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash));
  if(broken.length) throw new Error('Broken local anchors '+JSON.stringify(broken));
  fs.writeFileSync(output+'/report.json',JSON.stringify(reports,null,2));
  console.log('PASS: '+reports.length+' desktop/mobile page and puzzle checks; audience jump and local anchors.');
  await browser.close();
  server.kill();
})().catch(error=>{console.error(error.message);process.exit(1);});
