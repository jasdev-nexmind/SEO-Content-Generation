<template>
  <div>
    <LayoutHeader />

    <LayoutBanner_CenteredTextFullImage />

    <LayoutBanner_ImageRight />

    <LayoutCards_3Columns />

    <LayoutForm_ContactUs />

    <LayoutGallery_4Columns />

    <LayoutForm_ContactUs2 />

    <LayoutForm_FAQ />
  </div>
</template>
<script>
import LayoutHeader from "../Layouts/Layout-Header.vue";
import LayoutBanner_CenteredTextFullImage from "../Layouts/Layout-Banner_CenteredTextFullImage.vue";
import LayoutBanner_ImageRight from "../Layouts/Layout-Banner_ImageRight.vue";
import LayoutCards_3Columns from "../Layouts/Layout-Cards_3Columns.vue";
import LayoutForm_ContactUs from "../Layouts/Layout-ContactUs.vue";
import LayoutForm_ContactUs2 from "../Layouts/Layout-ContactUs2.vue";

import LayoutForm_FAQ from "../Layouts/Layout-FAQ.vue";
import LayoutGallery_4Columns from "../Layouts/Layout-Gallery_4Columns.vue";
import jsonData from '../content/Apple.json';

export default {
  name: "Layouts",
  components: {
    LayoutHeader,
    LayoutBanner_CenteredTextFullImage,
    LayoutBanner_ImageRight,
    LayoutCards_3Columns,
    LayoutForm_ContactUs,
    LayoutForm_FAQ,
    LayoutGallery_4Columns,
    LayoutForm_ContactUs2,
  },
  data() {
    return {
      isExpanded: false,
      myJsonData: jsonData

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
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  box-shadow: transparent;
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #4d4d4d;
  border-radius: 0px;
  border-left: 0px solid transparent;
  border-top: 0px solid transparent;
  border-bottom: 0px solid transparent;
}
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
.banner-sm {
  height: 500px;
}
.banner-md {
  height: 600px;
}
.banner-full {
  height: 100%;
}
.section__width-xl {
  max-width: 1600px;
}
.section__width-lg {
  max-width: 1200px;
}
.section__width-md {
  max-width: 900px;
}
.section__width-sm {
  max-width: 500px;
}
.section__padding-xl {
  padding: 6rem 0rem;
}
.section__padding-lg {
  padding: 4rem 0rem;
}
.section__padding-md {
  padding: 2rem 0rem;
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

@media (max-width: 991px) {
  ::-webkit-scrollbar {
    display: none;
  }

  .hero-banner {
    margin: 0rem auto;
    padding: 5rem 3rem 3rem;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  .banner-full,
  .banner-sm,
  .banner-md {
    height: auto;
  }
  .nex__herobanner__text {
    padding: 1rem 0rem 3rem;
  }
}

@media (max-width: 480px) {
  ::-webkit-scrollbar {
    display: none;
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
</style>
