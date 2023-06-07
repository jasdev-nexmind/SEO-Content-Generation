<template>
  <div>
    <section class="bg-lightgray">
      <div class="banner__sidebyside">
        <div class="banner__text">
          <div>
            <h1 class="banner__heading">Title Lorem Ipsum</h1>
            <h5 class="banner_subheading">Lorem Ipsum is simply dummy text of the typesetting industry.</h5>
            <button class="button-primary">Call to Action</button>
          </div>
        </div>
        <div class="banner__image">
          <div class="img-wrapper">
            <img src="https://wnyheroes.org/wp-content/plugins/events-calendar-pro/src/resources/images/tribe-event-placeholder-image.svg" alt="" />
          </div>
        </div>
      </div>
      <!-- <div class="toolbar">Toolbar</div> -->
    </section>
  </div>
</template>
<script>
export default {
  name: "name",
  data() {
    return {};
  },
  methods: {
    toggleMenu() {
      this.isExpanded = !this.isExpanded;
    },
  },
};
</script>
<style lang="css" scoped>
.banner__sidebyside {
  margin: 0rem auto;
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 6rem 0rem;
  max-width: 1600px;
}
.bg-lightgray {
  background-color: #f7f6f6;
}
/* text */
.banner__text {
  /* border: 1px solid red; */
  padding: 1rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  text-align: start;
}
.banner__heading {
  /* border: 1px solid rgb(70, 70, 72); */
  font-size: 4rem;
  margin: auto;
  margin-bottom: 2rem;
  color: #333333;
  text-align: start;
}
.banner_subheading {
  /* border: 1px solid rgb(24, 24, 26); */
  margin: auto;
  font-weight: normal;
  margin-bottom: 2rem;
  color: #4d4d4d;
  text-align: start;
}

/* image */
.banner__image {
  /* border: 1px solid blue; */
  display: grid;
  place-items: center;
}
.banner__image .img-wrapper {
  display: flex;
}
.banner__image img {
  object-fit: contain;
  max-width: 100%;
  border: 2px solid #4d505b;
  border-radius: 16px;
}
/* image full */
.banner__image-full {
  border: 1px solid blue;
  display: flex;
}
.banner__image-full .img-wrapper {
  display: flex;
}
.banner__image-full img {
  object-fit: contain;
  max-width: 100%;
  border: 2px solid #4d505b;
  border-radius: 16px;
}
@media (max-width: 991px) {
  .banner__sidebyside {
    margin: 0rem auto;
    padding: 5rem 3rem 3rem;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .banner__text {
    padding: 1rem 0rem 3rem;
  }
}
@media (max-width: 480px) {
  .banner__sidebyside {
    padding: 4rem 2rem;
  }

  .banner__text h1 {
    font-size: 3rem;
    text-align: start;
  }
}

/* layouts css */
.button-primary {
  border-radius: 6px;
  border: 1px solid transparent;
  padding: 0.5rem 1rem;
  background-color: rgb(66, 66, 66);
  color: #fff;
  font-weight: 600;
  transition: 0.2s ease-out;
}
.button-primary:hover {
  border: 1px solid transparent;
  background-color: rgb(42, 42, 42);
  transition: 0.2s ease-out;
  color: #fff;
}

.button-secondary {
  border-radius: 6px;
  border: 1px solid transparent;
  padding: 0.5rem 1rem;
  background-color: rgb(104, 104, 104);
  color: #fff;
  font-weight: 200;
  transition: 0.2s ease-out;
}
.button-secondary:hover {
  border: 1px solid transparent;
  background-color: rgb(82, 82, 82);
  transition: 0.2s ease-out;
  color: #fff;
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
</style>
