<script>
import Loading from "@/components/Loading.vue";

export default {
  components: {Loading},
  props: {
    provider: Object,
    company: String,
    is_sepehr: Boolean,
  },
  data() {
    return {
      provider_data: this.provider,
      loading: false,
      load_image: false,
      done: false,
      recaptcha_image: "",
      recaptcha_code: "",
      show_error: false
    }
  },
  methods: {
    get_image() {
      if (!this.loading) {
        this.loading = true;
        const link = 'set-cookie/' + '?sepehr_name=' + this.provider_data.code;
        this.$http.get(link).then((r) => {
          this.loading = false;
          this.load_image = true;
          this.recaptcha_image = r.data.image;
        }).catch(() => {
          this.loading = false;
          this.load_image = false;
          this.done = false;
          this.show_error = false;
          this.recaptcha_image = "";
          this.recaptcha_code = "";
        });
        this.show_error = false;
      }
      return false;
    },
    submitForm(e) {
      e.preventDefault();
      if (!this.loading && String(this.recaptcha_code).length > 5) {
        this.loading = true;
        const body = {
          "sepehr_name": this.provider_data.code,
          "company": this.company,
          "recaptcha_code": this.recaptcha_code
        };
        this.$http.post('set-cookie/', body).then(() => {
          this.done = true;
          this.provider_data.valid = true;
          this.loading = false;
          this.provider.date = "همین الان";
        }).catch(() => {
          this.loading = false;
          this.load_image = false;
          this.done = false;
          this.show_error = false;
          this.recaptcha_image = "";
          this.recaptcha_code = "";
        });
        this.show_error = false;
      } else {
        this.show_error = true;
      }
    },
    submit_not_sepehr() {
      if (!this.loading) {
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.done = true;
        }, 3500);
      }
    }
  }
}
</script>

<template>
  <div class="row py-3 align-items-center cookie-item rounded" v-if="is_sepehr">
    <div class="col-2 col-md-1">
      <div :class='{"active-button": true, "is-valid": provider_data?.valid}'></div>
    </div>
    <div class="col-5 col-md-2 d-flex align-items-center">
      <p class="m-0 ms-2">{{ provider_data?.name }}</p>
      <div v-if="provider_data.has_sign" class="has_sign d-flex justify-content-center align-items-center active">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#fff" class="bi bi-check"
             viewBox="0 0 16 16">
          <path
              d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
        </svg>
      </div>
      <div v-else class="has_sign d-flex justify-content-center align-items-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" fill="#fff" class="bi bi-x-lg"
             viewBox="0 0 16 16">
          <path
              d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
        </svg>
      </div>
    </div>
    <div class="col-5 col-md-3">
      <p class="m-0 dir-ltr">{{ provider?.date }}</p>
    </div>
    <div class="col-12 mt-3 mt-md-0 col-md-6">
      <div v-if="done">
        <div class="alert alert-success m-0 text-center">
          <h5 class="m-0">با موفقیت ثبت شد</h5>
        </div>
      </div>
      <form v-on:submit="submitForm" class="d-flex align-items-center justify-content-between" v-else-if="load_image">
        <img :src="recaptcha_image" class="img-fluid" alt="recaptcha image">
        <input type="number" class="form-control mx-2" :class="{'border-danger': show_error}" placeholder="کد تایید"
               :disabled="loading"
               v-model="recaptcha_code" min="0" max="999999999">
        <button type="submit" class="btn btn-success px-4">
          <loading v-if="loading"></loading>
          <span v-else>ثبت</span>
        </button>
      </form>
      <button class="btn btn-primary btn-sm" v-else v-on:click="get_image" :disabled="false">
        <loading v-if="loading"></loading>
        <span v-else>نمایش عکس</span>
      </button>
    </div>
  </div>
  <div class="row py-3 align-items-center cookie-item rounded" v-else>
    <div class="col-2 col-md-1">
      <div :class='{"active-button": true, "is-valid": provider_data?.valid}'></div>
    </div>
    <div class="col-5 col-md-2 d-flex">
      <p class="m-0">{{ provider_data?.name }}</p>
    </div>
    <div class="col-5 col-md-3">
      <p class="m-0 dir-ltr">{{ provider?.date }}</p>
    </div>
    <div class="col-12 mt-3 mt-md-0 col-md-6">
      <div class="alert alert-success m-0 text-center" v-if="done">
        <h5 class="m-0">با موفقیت ثبت شد</h5>
      </div>
      <button v-on:click="submit_not_sepehr" class="btn btn-success px-4" v-else>
        <loading v-if="loading"></loading>
        <span v-else>ثبت</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.active-button, .has_sign {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #dc3545;
}

.active-button.is-valid, .has_sign.active {
  background: #28a745;
}

.cookie-item:nth-child(odd) {
  background: #dee3e7;
}
</style>