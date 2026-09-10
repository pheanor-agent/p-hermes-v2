/* Blog reading enhancement. Previous URLs preserve section anchors. */
(() => {
  'use strict';
  const body=document.body;
  if(body.dataset.blogUrl){
    const destination=new URL(body.dataset.blogUrl,location.href);
    destination.hash=location.hash;
    location.replace(destination.href);
    return;
  }
  body.classList.add('js-enabled');
  document.getElementById('print-page')?.addEventListener('click',()=>window.print());
})();
