<template>
  <div>
    <section>
      <header>
        <div class="header-wrapper">
          <a href="#" class="header-logo-link">
            <img class="header-logo" src="https://cdn.shopify.com/s/files/1/0097/2075/8332/files/logo_shoes_black.png?v=1676026182" alt="Logo" />
          </a>
          <ul class="navigation">
            <li><a href="#">Home</a></li>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">Sign Up</a></li>
            <li><a href="#">Contact Us</a></li>
          </ul>
          <button class="button-sidebar">
            <div class="button-sidebar-icon"><span class="material-icons-outlined" @click="isExpanded = !isExpanded"> menu </span></div>
          </button>
        </div>
      </header>

      <aside :class="{ isExpanded: isExpanded }">
        <div class="mobile-sidebar-content">
          <button class="button-sidebar">
            <div class="button-sidebar-icon"><span class="material-icons-outlined btn-close" @click="isExpanded = !isExpanded"> clear </span></div>
          </button>
          <ul class="navigation-mobile">
            <li><a href="#">Home</a></li>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">Sign Up</a></li>
            <li><a href="#">Contact Us</a></li>
          </ul>
        </div>
      </aside>
      <div class="header-padding"></div>

      <!-- <div class="toolbar">Toolbar</div> -->
    </section>
  </div>
</template>
<script>
export default {
  name: "Layout_Header",
  data() {
    return {
      isExpanded: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isExpanded = !this.isExpanded;
    },
  },
};
</script>
<style lang="css" scoped>
/* header css */
.header-padding {
  display: block;
  padding-top: 6rem;
}
header {
  height: 6rem;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;
  z-index: 10;
  background-color: #fff;
  border-bottom: 2px solid #f7f6f6 !important;
}
.header-wrapper {
  display: flex;
  align-items: center;
  width: 1600px;
  padding: 0rem 3rem;
  margin: auto;
  align-items: center;
}
.header-logo-link {
  margin-right: auto;
}
.header-logo {
  height: 50px;
  object-fit: contain;
}
header .navigation {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin: 10px 0;
}
header .navigation li {
  list-style: none;
  margin: 0 20px;
}

header .navigation li a {
  color: #333333;
  text-decoration: none;
  font-weight: 600;
  letter-spacing: 1px;
}

header .navigation li a {
  color: #333333;
  font-weight: 600;
  font-size: 1rem;
  display: inline-block;
  position: relative;
  text-decoration: none;
  padding-bottom: 0.3rem;
}
header .navigation li a::after {
  content: "";
  color: #333333;
  position: absolute;
  z-index: 10;
  width: 100%;
  transform: scaleX(0);
  border-radius: 5px;
  height: 0.12em;
  bottom: 0;
  left: 0;
  background: currentcolor;
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}
header .navigation li a:hover::after {
  height: 0.12em;
  transform: scaleX(1);
  transform-origin: bottom left;
}
.button-sidebar {
  display: none;
}
aside {
  display: none;
  visibility: hidden;
  translate: 500px;
  opacity: 0;
  transition: 0.4s ease-out;
}

.button-sidebar-icon {
  color: #333333;
}

@media (max-width: 991px) {
  ::-webkit-scrollbar {
    display: none;
  }
  header {
    height: auto;
  }
  .header-padding {
    padding-top: 10rem;
  }
  header .navigation {
    display: flex;
  }
  .header-wrapper {
    padding: 0rem 1rem;
    flex-direction: column;
  }
  .header-logo-link {
    margin: 0 auto;
  }
  .header-logo {
    margin: 2rem auto;
  }
  header .navigation {
    margin-bottom: 2rem;
  }
  .hero-banner {
    margin: 0rem auto;
    padding: 5rem 3rem 3rem;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .button-sidebar {
    margin-top: 0.4rem;
    display: block;
  }
  aside.isExpanded {
    display: flex;
    visibility: visible;
    position: absolute;
    z-index: 10;
    right: 0;
    top: 0;
    height: 100vh;
    width: 80vw;
    background-color: #fff;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 25px;
    translate: 0px;
    opacity: 1;
    transition: 0.4s ease-out;
  }
  .button-sidebar {
    margin-left: auto;
  }
  .button-sidebar .btn-close {
    font-size: 25px;
  }
  .navigation-mobile {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: start;
    margin-left: 3rem;
  }
  .navigation-mobile li {
    list-style: none;
    margin: 1rem 0;
  }

  .navigation-mobile li a {
    color: #333333;
    text-decoration: none;
    font-size: 25px;
    font-weight: 600;
    letter-spacing: 1px;
  }

  header {
    height: 4rem;
  }
  .header-wrapper {
    flex-direction: row;
  }
  .header-logo-link {
    margin-left: 0;
    margin-right: auto;
  }
  .header-logo {
    height: 20px;
    margin: 1rem 0rem;
    object-fit: contain;
  }
  header .navigation {
    display: none;
  }
  .hero-banner {
    padding: 5rem 2rem 3rem;
  }
  .header-padding {
    padding-top: 4rem;
  }
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
  .nex__herobanner__text h1 {
    font-size: 3rem;
    text-align: start;
  }
  .article-section {
    padding: 2rem;
  }
  .mobile-sidebar-content {
    width: 80vw;
  }
}

/* App css */
.toolbar {
  display: none;
  background-color: azure;
  position: absolute;
  left: 50%;
}
section:hover .toolbar {
  display: block;
}
</style>
