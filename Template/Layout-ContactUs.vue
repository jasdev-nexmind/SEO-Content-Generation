<template>
  <div>
    <section class="bg-blurrylights">
      <div class="banner__sidebyside">
        <div class="banner__text">
          <div>
            <h1 class="banner__heading">Have a question?</h1>
            <h4 class="banner_subheading">Contact us if you have any questions!</h4>
          </div>
        </div>
        <div>
          <div class="input-card">
            <form action="">
              <div class="input">
                <input class="input__field" id="firstname" type="text" required />
                <label for="firstname" class="input__label">First Name</label>
              </div>
              <div class="input">
                <input class="input__field" id="lastname" type="text" required />
                <label for="lastname" class="input__label">Last Name</label>
              </div>
              <div class="input">
                <input class="input__field" id="email" type="email" required />
                <label for="email" class="input__label">Email Address</label>
              </div>
              <div class="input">
                <input class="input__field" id="phone" type="tel" required />
                <label for="phone" class="input__label">Phone</label>
              </div>
              <div class="textarea">
                <textarea class="input__field" id="question" type="textarea" required />
                <label for="question" class="input__label">Question</label>
              </div>

              <button type="submit" value="Submit" class="button-primary ms-auto">Submit</button>
            </form>
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
.input-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 3rem 2rem 2rem;
  width: 500px;
  margin-left: 5rem;
}
.input-card form {
  width: 100%;
  display: flex;
  flex-direction: column;
}
.input {
  position: relative;
  margin-bottom: 2rem;
}
.textarea {
  position: relative;
  margin-bottom: 1rem;
}
.input__field {
  padding: 10px;
  border: 1px solid #838383;
  border-radius: 4px;
  background-color: transparent;
  outline: 2px solid #fff;
  width: 100%;
}
.input__label {
  position: absolute;
  top: 0;
  left: 0;
  transform: translate(10px, 12px);
  transform-origin: left;
  transition: transform 0.25s;
  color: #838383;
}
.input__field:focus-visible ~ .input__label,
.input__field:valid ~ .input__label {
  transform: translate(0, -25px) scale(0.8);
  color: #838383;
}

.banner__sidebyside {
  margin: 0rem auto;
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 6rem 0rem;
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
  color: #fff;
  text-align: start;
}
.banner_subheading {
  /* border: 1px solid rgb(24, 24, 26); */
  margin: auto;
  font-weight: normal;
  margin-bottom: 2rem;
  color: #282828;
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
    margin: auto;
  }
  .input-card {
    width: auto;
    max-width: 500px;
    margin: auto;
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
  .input-card {
    width: auto;
    margin-left: auto;
  }
  .bg-blurrylights {
    background-size: cover;
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
