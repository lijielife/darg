function trackClick(name) {
  ga('send', 'event', 'buttons', 'click', name);
  console.log(name)
  return
};

// init bootstrap popover outside of angular env
$('[data-toggle="popover"]').popover();
