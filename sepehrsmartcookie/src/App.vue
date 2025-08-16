<script>
import MainLoading from "@/components/MainLoading.vue";
import CookieItem from "@/components/CookieItem.vue";

export default {
  components: {CookieItem, MainLoading},
  data() {
    return {
      companies: [],
      providers: [],
      selected_company: "",
      loading: false,
      show_select_company: true
    }
  },
  methods: {
    getData() {
      this.loading = true
      let url;
      if (this.selected_company) {
        url = `cookie-providers/?show_company=1&company_u_id=${this.selected_company}`;
      } else {
        url = `cookie-providers/?show_company=1`;
      }
      this.$http.get(url).then((r) => {
        const data = r.data;
        this.companies = data.companies;
        this.providers = data.providers;
      }).finally(() => {
        this.loading = false;
      })
    },
    setCompanyGetData() {
      if (this.selected_company){
        this.show_select_company = false;
        this.getData();
      }
    }
  },
  mounted() {
    this.$http.get('get-company-list/').then((r) => {
      this.companies = r.data;
    })
  }
}
</script>

<template>
  <section v-if="show_select_company" class="w-100 h-100">
    <div class="container">
      <h1 class="text-center my-3 mt-5">اکانت خود را انتخاب کنید</h1>
      <hr>
      <select class="form-control" v-model="selected_company">
        <option value="" selected disabled>اکانت</option>
        <option :value="company.u_id" v-for="(company, index) in companies" :key="index">{{ company.name }}</option>
      </select>
      <button class="btn btn-success w-100 mt-3" v-on:click="setCompanyGetData">گرفتن داده</button>
    </div>
  </section>
  <section v-else>
    <div class="w-50 mx-auto" v-if="loading">
      <main-loading></main-loading>
    </div>
    <div class=" py-3" v-else style="width: 85%; margin: 0 auto">
      <!-- ---- HEADER ---- -->
      <div class="row py-3 align-items-center bg-dark text-light sticky-top rounded">
        <div class="col-12 col-md-1 d-none d-md-block">
          <h5 class="m-0">فعال</h5>
        </div>
        <div class="col-12 col-md-2 d-none d-md-block">
          <h5 class="m-0">نام</h5>
        </div>
        <div class="col-12 col-md-3 d-none d-md-block">
          <h5 class="m-0">آخرین آپدیت</h5>
        </div>
        <div class="col-12 col-md-3 d-none d-md-block">
          <h5 class="m-0">عملیات</h5>
        </div>
        <div class="col-12 col-md-3">
          <select class="form-control" v-model="selected_company" v-on:change="getData">
            <option :value="company.u_id" v-for="(company, index) in companies" :key="index">{{ company.name }}</option>
          </select>
        </div>
      </div>
      <!-- ---- DATA ---- -->
      <cookie-item v-for="(provider, index) in providers" :key="index" :provider="provider"
                   :company="selected_company" :is_sepehr="true"></cookie-item>
      <cookie-item :provider="{name: 'آلوین', date: '0', valid: true}" :company="selected_company"
                   :is_sepehr="false"></cookie-item>
      <cookie-item :provider="{name: 'دلتابان', date: '0', valid: true}" :company="selected_company"
                   :is_sepehr="false"></cookie-item>
      <cookie-item :provider="{name: 'بوکینگ', date: '0', valid: true}" :company="selected_company"
                   :is_sepehr="false"></cookie-item>
    </div>
  </section>
</template>

<style>
body {
  direction: rtl;
}

.sticky-top {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
}
</style>
