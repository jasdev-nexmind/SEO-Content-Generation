<template>
  <div>
    <section class="bg-nexmind-blue">
      <div class="banner__sidebyside">
        <div class="banner__text">
          <div>
            <h2 class="banner__heading mb-0">Title Lorem Ipsum</h2>
            <hr class="custom__hr" />
            <ul class="list__info">
              <li>Point 1</li>
              <li>Point 2</li>
              <li>Point 3</li>
              <li>Point 4</li>
              <li>Point 5</li>
              <li>Point 6</li>
              <li>Point 7</li>
              <li>Point 8</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="input-card">
            <h4>Tell us a bit about yourself and your needs for a personalized experience.</h4>
            <form action="" class="form__inputgroup mt-4">
              <div class="input">
                <input class="input__field" id="firstname" type="text" required />
                <label for="firstname" class="input__label">First Name</label>
              </div>
              <div class="input">
                <input class="input__field" id="lastname" type="text" required />
                <label for="lastname" class="input__label">Last Name</label>
              </div>
              <div class="input">
                <input class="input__field" id="email2" type="email" required />
                <label for="email2" class="input__label">Email Address</label>
              </div>
              <div class="input">
                <input class="input__field" id="phone2" type="tel" required />
                <label for="phone2" class="input__label">Phone</label>
              </div>
              <!-- <div class="textarea">
                <textarea class="input__field" id="question" type="textarea" required />
                <label for="question" class="input__label">Question</label>
              </div> -->
              <div class="">
                <select name="Country" id="" class="input__field">
                  <option selected disabled>Country</option>
                  <option>Malaysia</option>
                  <option>Australia</option>
                  <option>Singapore</option>
                  <option>...</option>
                </select>
                <!-- <label for="phone2" class="input__label">Phone</label> -->
              </div>
              <h6 class="mt-4">How did you hear about us?</h6>
              <div class="layoutform_inputgroup__radio input-group mt-1 mb-3">
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="google" value="google" v-validate="'required'" />
                  <label class="form-check-label" for="google">Google</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="facebook" value="facebook" v-validate="'required'" />
                  <label class="form-check-label" for="facebook">Facebook</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="linkedin" value="linkedin" v-validate="'required'" />
                  <label class="form-check-label" for="linkedin">LinkedIn</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="e-mail" value="e-mail" v-validate="'required'" />
                  <label class="form-check-label" for="e-mail">Email</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="quora" value="quora" v-validate="'required'" />
                  <label class="form-check-label" for="quora">Quora</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="reddit" value="reddit" v-validate="'required'" />
                  <label class="form-check-label" for="reddit">Reddit</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="medium" value="medium" v-validate="'required'" />
                  <label class="form-check-label" for="medium">Medium</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="website" id="others" value="others" v-validate="'required'" />
                  <label class="form-check-label" for="others">Others</label>
                </div>
              </div>
              <button type="submit" value="Submit" class="button button-purple w-100">Submit</button>
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
.w-100 {
  width: 100% !important;
}
.mb-0 {
  margin-bottom: 0 !important;
}
.mt-4 {
  margin-top: 2rem !important;
}
.color-white {
  color: white;
}
.custom__hr {
  border: none;
  height: 2px;
  background: #fff;
  opacity: 1;
}
.list__info {
  padding: 0;
}
.list__info li {
  font-size: 1rem;
  color: #fff;
  background: url(https://www.nexmind.ai/wp-content/uploads/2022/07/check.svg) no-repeat left center;
  padding: 5px 10px 5px 45px;
  list-style: none;
  /* margin: 0; */
  vertical-align: middle;
}
button {
  border-radius: 6px;
  border: 1px solid transparent;
  padding: 0.5rem 1rem;
  background-color: rgb(66, 66, 66);
  color: #fff;
  font-weight: 600;
  transition: 0.2s ease-out;
}
.button-purple {
  background-color: #a722e6;
}

.input-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 2rem;
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
  color: #838383 !important;
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
.bg-nexmind-blue {
  background-image: url("https://www.nexmind.ai/wp-content/uploads/2022/05/background01-scaled.jpg");
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

.layoutform_inputgroup__radio {
  display: flex;
  justify-content: start;
  user-select: none;
}
.layoutform_inputgroup__radio .form-check .form-check-input {
  visibility: hidden;
}
.layoutform_inputgroup__radio .form-check .form-check-label {
  transform: translate(-23px, 0px);
  border: 1px solid #a722e6;
  color: #a722e6;
  background-color: var(--white);
  border-radius: 20px;
  padding: 0.2rem 0.8rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
}
.layoutform_inputgroup__radio .form-check .form-check-label:hover {
  background-color: var(--light);
  border: 1px solid #a722e6;
  color: #a722e6;
  transition: all 0.3s ease-out;
}
.layoutform_inputgroup__radio .form-check .form-check-input:checked ~ .form-check-label {
  background-color: #a722e6;
  border: 1px solid #a722e6;
  color: var(--white);
  transition: all 0.3s ease-out;
}
</style>
