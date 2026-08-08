// theme
(function(){
  var t = localStorage.getItem('dc-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', t);
})();
function toggleTheme(){
  var d = document.documentElement;
  var t = d.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
  d.setAttribute('data-theme', t);
  localStorage.setItem('dc-theme', t);
}

document.addEventListener('DOMContentLoaded', function(){
  // copy buttons
  document.querySelectorAll('pre').forEach(function(pre){
    var b = document.createElement('button');
    b.className = 'copy'; b.textContent = 'copy';
    b.onclick = function(){
      navigator.clipboard.writeText(pre.querySelector('code').innerText);
      b.textContent = 'copied'; setTimeout(function(){ b.textContent='copy'; }, 1200);
    };
    pre.appendChild(b);
  });

  // reading progress
  var bar = document.createElement('div');
  bar.className = 'progress';
  document.body.appendChild(bar);
  window.addEventListener('scroll', function(){
    var h = document.documentElement;
    var p = h.scrollTop / (h.scrollHeight - h.clientHeight) * 100;
    bar.style.width = (p || 0) + '%';
  });

  // quiz
  document.querySelectorAll('.quiz').forEach(function(q){
    var ans = q.dataset.answer;
    q.querySelectorAll('button').forEach(function(btn){
      btn.onclick = function(){
        var ok = btn.dataset.opt === ans;
        btn.classList.add(ok ? 'right' : 'wrong');
        if (ok) q.querySelectorAll('button').forEach(function(b){ b.disabled = true; });
        var fb = q.querySelector('.fb');
        if (fb) fb.style.display = 'block';
      };
    });
  });
});
