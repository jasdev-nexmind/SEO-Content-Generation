<template>
  <div>
    <section class="bg-lightgray">
      <div class="banner__centered">
        <div class="banner__text">
          <h2 class="banner__heading">Frequently Asked Questions</h2>
        </div>
        <div class="collapsible__section">
          <div class="faq-collabsible" v-for="n in 5" :key="n">
            <input :id="'collapsible' + n" class="toggle" type="checkbox" />
            <label :for="'collapsible' + n" class="lbl-toggle">Question {{ n }}</label>
            <div class="collapsible-content">
              <div class="content-inner">
                <p>
                  Bacon ipsum dolor amet pork belly capicola ground round brisket. Shank pork belly cupim fatback. Flank porchetta chicken spare ribs. Ham prosciutto pork belly
                  turkey beef picanha strip steak swine alcatra.
                </p>
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
      n: 1,
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
input[type="checkbox"] {
  display: none;
}
.collapsible__section {
  max-width: 900px;
  margin: 0 auto;
}
.faq-collabsible {
  border-bottom: 1px solid rgba(62, 62, 62, 0.45);
}
.lbl-toggle {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1.2rem;
  text-align: start;
  padding: 1rem;
  color: #333333;
  cursor: pointer;
  transition: all 0.25s ease-out;
  /* border-bottom: 1px solid rgba(62, 62, 62, 0.45); */
}
.lbl-toggle:hover {
  color: #000;
}
.lbl-toggle::after {
  height: 10px;
  content: " ";
  display: inline-block;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 5px solid currentColor;
  vertical-align: middle;
  /* margin-right: 0.7rem; */
  transform: translateY(-2px);
  transition: transform 0.2s ease-out;
  margin-left: auto;
}
.toggle:checked + .lbl-toggle::after {
  transform: rotate(90deg) translateX(-3px);
}
/* .toggle:checked + .lbl-toggle {
  border-bottom: 1px solid transparent;
} */
.collapsible-content {
  max-height: 0px;
  overflow: hidden;
  transition: max-height 0.25s ease-in-out;
}
.toggle:checked + .lbl-toggle + .collapsible-content {
  max-height: 350px;
}
/* .toggle:checked + .lbl-toggle {
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
} */
.collapsible-content .content-inner {
  /* border-bottom: 1px solid rgba(62, 62, 62, 0.45); */
  padding: 0.5rem 1rem;
}
.collapsible-content p {
  margin-bottom: 0;
}
.banner__centered {
  margin: 0rem auto;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 4rem 0rem;
  max-width: 1400px;
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.banner__heading {
  font-size: 3rem;
  margin: auto;
  margin-bottom: 2rem;
  color: #333333;
  text-align: center;
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
    margin: auto;
  }
}
@media (max-width: 480px) {
  .collapsible__section {
    max-width: 900px;
  }
  .banner__centered {
    padding: 4rem 2rem;
  }
  /* .banner__text {
    padding: 0rem 2rem;
    margin-bottom: 1rem;
  } */

  .banner__text h2 {
    font-size: 2rem;
    text-align: center;
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
