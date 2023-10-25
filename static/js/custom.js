(function() {
  "use strict";

  function toggleSidebar() {
      document.body.classList.toggle("sidebar-toggled");
      document.querySelector(".sidebar").classList.toggle("toggled");

      if (document.querySelector(".sidebar").classList.contains("toggled")) {
          const collapseElements = document.querySelectorAll('.sidebar .collapse');
          for (let i = 0; i < collapseElements.length; i++) {
              collapseElements[i].classList.remove("show");
          }
      }
  }

  function resizeWindow() {
      if (window.innerWidth < 768) {
          const collapseElements = document.querySelectorAll('.sidebar .collapse');
          for (let i = 0; i < collapseElements.length; i++) {
              collapseElements[i].classList.remove("show");
          }
      }

      if (window.innerWidth < 480 && !document.querySelector(".sidebar").classList.contains("toggled")) {
          document.body.classList.add("sidebar-toggled");
          document.querySelector(".sidebar").classList.add("toggled");
          const collapseElements = document.querySelectorAll('.sidebar .collapse');
          for (let i = 0; i < collapseElements.length; i++) {
              collapseElements[i].classList.remove("show");
          }
      }
  }

  function handleMouseWheel(e) {
      if (window.innerWidth > 768) {
          const delta = e.wheelDelta || -e.detail;
          this.scrollTop += (delta < 0 ? 1 : -1) * 30;
          e.preventDefault();
      }
  }

  function handleScroll() {
      const scrollDistance = window.scrollY || document.documentElement.scrollTop;
      const scrollButton = document.querySelector('.scroll-to-top');
      if (scrollDistance > 100) {
          scrollButton.style.display = "block";
      } else {
          scrollButton.style.display = "none";
      }
  }

  function scrollToTop(e) {
      e.preventDefault();
      const anchor = this.getAttribute('href');
      const targetElement = document.querySelector(anchor);
      if (targetElement) {
          const offsetTop = targetElement.offsetTop;
          window.scrollTo({
              top: offsetTop,
              behavior: 'smooth'
          });
      }
  }

  document.querySelector("#sidebarToggle")?.addEventListener('click', toggleSidebar);
  document.querySelector("#sidebarToggleTop")?.addEventListener('click', toggleSidebar);

  window.addEventListener('resize', resizeWindow);

  const fixedNavSidebar = document.querySelector('body.fixed-nav .sidebar');
  fixedNavSidebar?.addEventListener('mousewheel', handleMouseWheel);
  fixedNavSidebar?.addEventListener('DOMMouseScroll', handleMouseWheel);
  fixedNavSidebar?.addEventListener('wheel', handleMouseWheel);

  document.addEventListener('scroll', handleScroll);

  const scrollButton = document.querySelector('.scroll-to-top');
  if (scrollButton) {
      scrollButton.addEventListener('click', scrollToTop);
  }
})();
