(function () {
  'use strict';

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    Object.defineProperty(Constructor, "prototype", {
      writable: false
    });
    return Constructor;
  }

  var Navigation = /*#__PURE__*/function () {
    function Navigation(options) {
      _classCallCheck(this, Navigation);

      this.maxHeight = undefined;
      this.el = options.element;
      var self = this;

      if (this.el.getAttribute('data-set-max-height')) {
        this.el.style.maxHeight = 0;
        var observer = new MutationObserver(function () {
          self.update();
        });
        observer.observe(self.el, {
          attributes: true,
          attributeFilter: ['class'],
          childList: false,
          characterData: false
        });
      }
    }

    _createClass(Navigation, [{
      key: "getHeight",
      value: function getHeight() {
        var h;
        var maxHeight = this.el.style.maxHeight;
        this.el.style.maxHeight = 'none';
        h = this.el.offsetHeight;
        this.el.style.maxHeight = maxHeight;
        return h;
      }
    }, {
      key: "update",
      value: function update() {
        var self = this;

        if (this.el.classList.contains('is-visible')) {
          if (this.maxHeight === undefined) {
            this.maxHeight = this.getHeight();
          } //wihtout setTimeout style change won't be animated


          setTimeout(function () {
            self.el.style.maxHeight = self.maxHeight + 'px';
          }, 0);
        } else {
          this.el.style.maxHeight = 0;
        }
      }
    }]);

    return Navigation;
  }();

  var Accordion = /*#__PURE__*/function () {
    function Accordion(el) {
      var _this = this;

      _classCallCheck(this, Accordion);

      // Store the <details> element
      this.el = el; // Store the <summary> element

      this.summary = el.querySelector('summary'); // Store the <div class="content"> element

      this.content = el.querySelector('.accordion__content'); // Store the animation object (so we can cancel it if needed)

      this.animation = null; // Store if the element is closing

      this.isClosing = false; // Store if the element is expanding

      this.isExpanding = false; // Detect user clicks on the summary element

      this.summary.addEventListener('click', function (e) {
        return _this.onClick(e);
      });
    }

    _createClass(Accordion, [{
      key: "onClick",
      value: function onClick(e) {
        // Stop default behaviour from the browser
        e.preventDefault(); // Add an overflow on the <details> to avoid content overflowing

        this.el.style.overflow = 'hidden'; // Check if the element is being closed or is already closed

        if (this.isClosing || !this.el.open) {
          this.open(); // Check if the element is being openned or is already open
        } else if (this.isExpanding || this.el.open) {
          this.shrink();
        }
      }
    }, {
      key: "shrink",
      value: function shrink() {
        var _this2 = this;

        // Set the element as "being closed"
        this.isClosing = true; // Store the current height of the element

        var startHeight = "".concat(this.el.offsetHeight, "px"); // Calculate the height of the summary

        var endHeight = "".concat(this.summary.offsetHeight, "px"); // If there is already an animation running

        if (this.animation) {
          // Cancel the current animation
          this.animation.cancel();
        } // Start a WAAPI animation


        this.animation = this.el.animate({
          // Set the keyframes from the startHeight to endHeight
          height: [startHeight, endHeight]
        }, {
          duration: 400,
          easing: 'ease-out'
        }); // When the animation is complete, call onAnimationFinish()

        this.animation.onfinish = function () {
          return _this2.onAnimationFinish(false);
        }; // If the animation is cancelled, isClosing variable is set to false


        this.animation.oncancel = function () {
          return _this2.isClosing = false;
        };
      }
    }, {
      key: "open",
      value: function open() {
        var _this3 = this;

        // Apply a fixed height on the element
        this.el.style.height = "".concat(this.el.offsetHeight, "px"); // Force the [open] attribute on the details element

        this.el.open = true; // Wait for the next frame to call the expand function

        window.requestAnimationFrame(function () {
          return _this3.expand();
        });
      }
    }, {
      key: "expand",
      value: function expand() {
        var _this4 = this;

        // Set the element as "being expanding"
        this.isExpanding = true; // Get the current fixed height of the element

        var startHeight = "".concat(this.el.offsetHeight, "px"); // Calculate the open height of the element (summary height + content height)

        var endHeight = "".concat(this.summary.offsetHeight + this.content.offsetHeight, "px"); // If there is already an animation running

        if (this.animation) {
          // Cancel the current animation
          this.animation.cancel();
        } // Start a WAAPI animation


        this.animation = this.el.animate({
          // Set the keyframes from the startHeight to endHeight
          height: [startHeight, endHeight]
        }, {
          duration: 400,
          easing: 'ease-out'
        }); // When the animation is complete, call onAnimationFinish()

        this.animation.onfinish = function () {
          return _this4.onAnimationFinish(true);
        }; // If the animation is cancelled, isExpanding variable is set to false


        this.animation.oncancel = function () {
          return _this4.isExpanding = false;
        };
      }
    }, {
      key: "onAnimationFinish",
      value: function onAnimationFinish(open) {
        // Set the open attribute based on the parameter
        this.el.open = open; // Clear the stored animation

        this.animation = null; // Reset isClosing & isExpanding

        this.isClosing = false;
        this.isExpanding = false; // Remove the overflow hidden and the fixed height

        this.el.style.height = this.el.style.overflow = '';
      }
    }]);

    return Accordion;
  }();

  var html = document.querySelector('html');
  html.classList.remove('no-js');
  html.classList.add('js'); //taken from http://youmightnotneedjquery.com/

  function ready(fn) {

    if (document.attachEvent ? document.readyState === 'complete' : document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  ready(function () {

    console.log('DOM is ready!'); //initialize navigation

    var nav = new Navigation({
      element: document.querySelector('header > nav')
    }); //hamburger button

    var hamburger = document.querySelector('button.hamburger');

    if (hamburger) {
      hamburger.addEventListener('click', function () {
        hamburger.classList.toggle('is-active');

        if (nav.el) {
          nav.el.classList.toggle('is-visible');
        }
      });
    } //example of using a handlebars template/partial


    Handlebars.registerPartial('myPartial', myApp.templates.myPartial);
    var template = myApp.templates.helloWorld;
    var html = template({
      'title': 'Example of markup generated via js using handlebars',
      'subtitle': 'This text comes from a hbs partial!'
    });
    var aside = document.querySelector('aside') || document.querySelector('.handlebars');

    if (aside) {
      aside.innerHTML = html;
    } else {
      console.log('aside not found!');
    } //initialize accordions


    document.querySelectorAll('.accordion').forEach(function (el) {
      new Accordion(el);
    });
  });

})();
