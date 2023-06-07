<template>
  <div>
    <div class="lightbox-target" id="1">
      <img src="https://via.placeholder.com/150" />
      <a class="lightbox-close" href="#"></a>
    </div>
    <section class="bg-lightgray">
      <div class="gallery-section section__width-xl">
        <div class="banner__text">
          <h2 class="banner__heading">Gallery</h2>
        </div>
        <div class="gallery__section">
          <!-- <a class="lightbox" href="#1"><img src="https://via.placeholder.com/150" /></a> -->

          <div class="lightbox-gallery">
            <div class="container">
              <div class="row">
                <div class="col-sm-6 col-md-4 col-lg-3 mb-4" v-for="image in images" :key="image">
                  <a href="#"><img class="img-fluid" :src="image.url" :alt="image.alt" /></a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  name: "name",
  data() {
    return {
      images: [
        { url: "https://i.imgur.com/zmzERpe.jpg", alt: "car" },
        { url: "https://i.imgur.com/gX11Vt5.jpg", alt: "car" },
        { url: "https://i.imgur.com/pZcUS2Y.jpg", alt: "car" },
        { url: "https://i.imgur.com/06Ajq7f.jpg", alt: "car" },
        { url: "https://i.imgur.com/zmzERpe.jpg", alt: "car" },
        { url: "https://i.imgur.com/gX11Vt5.jpg", alt: "car" },
        { url: "https://i.imgur.com/pZcUS2Y.jpg", alt: "car" },
        { url: "https://i.imgur.com/06Ajq7f.jpg", alt: "car" },
      ],
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
.bg-lightgray {
  background-color: #f7f6f6;
}
.gallery-section {
  margin: 0rem auto;
  padding: 4rem;
  max-width: 1600px;
  height: 100%;
}
.banner__text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin-bottom: 3rem;
}
.banner__heading {
  font-size: 3rem;
  margin: auto;
  color: #333333;
  text-align: center;
}

.grid {
  width: 100%;
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
}
/* .cell {
  border: 1px solid #333333;
} */

@media (max-width: 480px) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
  .gallery-section {
    margin: 0rem auto;
    padding: 4rem 2rem;
  }
}

.toolbar {
  display: none;
  background-color: azure;
  position: absolute;
  left: 50%;
}
section:hover .toolbar {
  display: block;
}

/* Bootstrap css */
.row {
  --bs-gutter-x: 1.5rem;
  --bs-gutter-y: 0;
  display: flex;
  flex-wrap: wrap;
  margin-top: calc(-1 * var(--bs-gutter-y));
  margin-right: calc(-0.5 * var(--bs-gutter-x));
  margin-left: calc(-0.5 * var(--bs-gutter-x));
}

@media (max-width: 992px) {
  .col-lg-3 {
    flex: 0 0 auto;
    width: 25%;
  }
}

@media (max-width: 768px) {
  .col-md-4 {
    flex: 0 0 auto;
    width: 33.33333333%;
  }
}
@media (max-width: 576px) {
  .col-sm-6 {
    flex: 0 0 auto;
    width: 50%;
  }
}
.mb-4 {
  margin-bottom: 1.5rem !important;
}
/*  */

a.lightbox img {
  height: 150px;
  border: 3px solid white;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
  margin: 94px 20px 20px 20px;
}

/* Styles the lightbox, removes it from sight and adds the fade-in transition */

.lightbox-target {
  position: fixed;
  z-index: 11;
  top: -100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.7);
  width: 100%;
  opacity: 0;
  -webkit-transition: opacity 0.5s ease-in-out;
  -moz-transition: opacity 0.5s ease-in-out;
  -o-transition: opacity 0.5s ease-in-out;
  transition: opacity 0.5s ease-in-out;
  overflow: hidden;
}

/* Styles the lightbox image, centers it vertically and horizontally, adds the zoom-in transition and makes it responsive using a combination of margin and absolute positioning */

.lightbox-target img {
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  max-height: 0%;
  max-width: 0%;
  border: 3px solid white;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
  -webkit-transition: 0.5s ease-in-out;
  -moz-transition: 0.5s ease-in-out;
  -o-transition: 0.5s ease-in-out;
  transition: 0.5s ease-in-out;
}

/* Styles the close link, adds the slide down transition */

a.lightbox-close {
  display: block;
  width: 50px;
  height: 50px;
  box-sizing: border-box;
  background: rgb(255, 255, 255);
  color: black;
  text-decoration: none;
  position: absolute;
  top: 1rem;
  right: 1rem;
  -webkit-transition: 0.5s ease-in-out;
  -moz-transition: 0.5s ease-in-out;
  -o-transition: 0.5s ease-in-out;
  transition: 0.5s ease-in-out;
}

/* Provides part of the "X" to eliminate an image from the close link */

a.lightbox-close:before {
  content: "";
  display: block;
  height: 30px;
  width: 1px;
  background: black;
  position: absolute;
  left: 26px;
  top: 10px;
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  transform: rotate(45deg);
}

/* Provides part of the "X" to eliminate an image from the close link */

a.lightbox-close:after {
  content: "";
  display: block;
  height: 30px;
  width: 1px;
  background: black;
  position: absolute;
  left: 26px;
  top: 10px;
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

/* Uses the :target pseudo-class to perform the animations upon clicking the .lightbox-target anchor */

.lightbox-target:target {
  opacity: 1;
  top: 0;
  bottom: 0;
  overflow: scroll;
}

.lightbox-target:target img {
  max-height: 100%;
  max-width: 100%;
}
</style>
