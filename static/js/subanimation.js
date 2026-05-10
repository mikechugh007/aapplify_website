const faqs = document.querySelectorAll(".faq");
faqs.forEach((faq) => {
  faq.addEventListener("click", () => {
    faq.classList.toggle("active");
  });
});

var gallerySwiper = new Swiper(".gallerySwiper", {
    slidesPerView: "auto",
    spaceBetween: 30,
    loop: true,
    cssMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    mousewheel: true,
    keyboard: true,
    centeredSlides: true,
  });

  var testimonialSwiper = new Swiper(".testimonialSwiper", {
    spaceBetween: 30,
    loop: true,
    cssMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    mousewheel: true,
    keyboard: true,
  });


  const scrollers = document.querySelectorAll(".scroller");

  function addScrollAnimation() {
    scrollers.forEach((scroller) => {
      scroller.setAttribute("data-animated", true);

      const scrollerInner = scroller.querySelector(".scroller_inner");
      const scrollerContent = Array.from(scrollerInner.children);

      scrollerContent.forEach((item) => {
        const duplicatedItem = item.cloneNode(true);
        duplicatedItem.setAttribute("aria-hidden", true);
        scrollerInner.appendChild(duplicatedItem);
      });
    });
  }

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    addScrollAnimation();
  }

  function heroAnimation() {
    var tl = gsap.timeline();
    tl.from("nav .logo, nav li, nav button, nav a", {
      y: -30,
      opacity: 0,
      duration: 0.2,
      stagger: 0.01,
    });
    tl.from(
      ".hero-part1 h1",
      {
        x: -200,
        opacity: 0,
        duration: 0.5,
      },
      "-=1"
    );
    tl.from(
      ".hero-part1 p",
      {
        x: -50,
        opacity: 0,
        duration: 0.4,
      },
      "-=0.5"
    );
    tl.from(".hero-part1 button", {
      opacity: 0,
      duration: 0.4,
    });
    tl.from(
      ".hero-part2",
      {
        x: 30,
        opacity: 0,
        duration: 0.5,
      },
      "-=0.7"
    );
  }

  function unlockAiAnimation() {
    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: ".unlockai",
        scroller: "body",
        start: "top 50%",
        end: "top -20%",
        scrub: 2,
      },
    });

    tl.from(".unlockai h1", {
      y: 50,
      opacity: 0,
      duration: 0.7,
    });
    tl.from(".unlockai p", {
      y: 50,
      opacity: 0,
      duration: 0.7,
    });
    tl.from(".unlockai img", {
      y: 50,
      opacity: 0,
      duration: 0.7,
    });
  }

  function introductionAnimation() {
    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: ".introduction",
        scroller: "body",
        start: "top 50%",
        end: "top -20%",
        scrub: 2,
      },
    });
    tl.from(".introduction h1", {
      y: 50,
      opacity: 0,
      duration: 0.7,
    });
    tl.from(".introduction .elem", {
      y: 50,
      opacity: 0,
      duration: 0.7,
      stagger: 0.3,
    });
  }

  heroAnimation();
  unlockAiAnimation();
  introductionAnimation();