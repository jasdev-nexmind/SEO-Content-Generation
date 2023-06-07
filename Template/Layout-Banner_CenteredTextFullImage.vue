<template>
  <div>
    <section class="bg-blurrylights">
      <div class="banner__centered">
        <div class="banner__text">
          <div class="d-flex flex-column">
            <h1 class="banner__heading">Title Lorem Ipsum</h1>
            <h5 class="banner_subheading">Lorem Ipsum is simply dummy text of the typesetting industry.</h5>
            <div class="mx-auto">
              <button class="button-primary">Call to Action</button>
              <button class="button-secondary ms-3">Call to Action</button>
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
.banner__centered {
  margin: 0rem auto;
  height: 100%;
  padding: 6rem 0rem;
  max-width: 1600px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 6rem);
}
.bg-lightgray {
  background-color: #f7f6f6;
}
.bg-blurrylights {
  background-image: url("https://images.unsplash.com/photo-1495422964407-28c01bf82b0d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80");
  background-repeat: no-repeat;
  background-size: 100% 130%;
}
/* text */
.banner__text {
  /* border: 1px solid red; */
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
  color: #232323;
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
  .banner__centered {
    margin: 0rem auto;
    padding: 5rem 3rem 3rem;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .banner__text {
    padding: 1rem 0rem 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .banner__heading {
    text-align: center;
  }
  .banner_subheading {
    text-align: center;
  }
}
@media (max-width: 480px) {
  .banner__centered {
    padding: 4rem 2rem;
  }

  .banner__text {
    padding: 1rem 0rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .banner__heading {
    font-size: 3rem;
    text-align: center;
  }
  .banner_subheading {
    text-align: center;
  }
  .bg-blurrylights {
    background-size: cover;
  }
}

/* layouts css */
.d-flex {
  display: flex !important;
}
.flex-column {
  flex-direction: column !important;
}
.mx-auto {
  margin: 0 auto !important;
}
.my-auto {
  margin: auto 0 !important;
}
.m-auto {
  margin: auto !important;
}
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
