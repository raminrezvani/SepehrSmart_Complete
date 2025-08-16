<template>
  <section>
    <!-- MAIN ITEM -->
    <div :class="{'border rounded p-3 shadow-xs mt-3': true, 'sticky-item': show}">
      <div class="row align-items-center">
        <!-- AIRLINE NAME -->
        <div class="col-12 col-md-4">
          <h5>{{ data.airline_name }}</h5>
          <h5 class="mt-2">{{ data.flight_number }}</h5>
        </div>
        <!-- GO FLIGHT -->
        <div class="col-6 col-md-2 mt-3 mt-md-0">
          <h5 class="mt-2">{{ data.go_time }}</h5>
          <h5 class="mt-2">{{ data.go_date }}</h5>
        </div>
        <!-- RETURN FLIGHT -->
        <div class="col-6 col-md-2 mt-3 mt-md-0">
          <h5 class="mt-2">{{ data.return_time }}</h5>
          <h5 class="mt-2">{{ data?.return_date }}</h5>
        </div>
        <!-- PRICE -->
        <div class="col-12 col-md-4 mt-3 mt-md-0">
          <div class="d-flex algin-items-center justify-content-between">
            <h5>قیمت هر نفر:</h5>
            <h5 class="text-center">{{ perPerson(data.price) }} تومان</h5>
          </div>
          <hr>
          <div class="d-flex algin-items-center justify-content-between">
            <h5>قیمت کل:</h5>
            <h5 class="text-center">{{ totalPerson(data.price) }} تومان</h5>
          </div>
        </div>
        <!-- MORE -->
        <div class="col-12 mt-3 ">
          <div class="row align-items-center">
            <div class="col-12 col-md-3">
              <h5 class="">{{ data.providers[0].provider_name }}</h5>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <button class="btn btn-info w-100" v-on:click="show = !show">
                <span>
<!--                  <i class="fa fa-spinner fa-spin" v-if="loading_analysis"></i>-->
                  نمایش آنالیز
                </span>
              </button>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <button class="btn btn-primary w-100" v-on:click="show = !show">
                <span v-if="show">بستن</span>
                <span v-else>سایر ({{ data.providers.length }})</span>
              </button>
            </div>
            <div class="col-12 col-md-3 mt-3 mt-md-0">
              <a target="_blank" :href="data.providers[0].buy_link" class="btn btn-success w-100">نمایش در سایت</a>
            </div>
          </div>
        </div>

        


        </div>
    </div>
    <!--    </div>-->
    <!-- COlLAPSE PROVIDER -->
    <div :class="{'collapse': true, 'show': show}" :id="unique_id">
      <div class="row">
        <div class="col-12 col-md-4 mt-4" v-for="(provider, index) in data.providers" :key="index">
          <div class="border p-3 rounded">
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider.provider_name }}</h5>
              <img :src="provider.provider_logo" :alt="provider.provider_name" width="35" height="35">
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider.go_date }}</h5>
              <h5 class="mt-2">{{ provider.go_time }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ provider?.return_date }}</h5>
              <h5 class="mt-2">{{ provider?.return_date }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <h5>تعداد صندلی</h5>
              <h5 class="mt-2">{{ provider.seat }}</h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>هر نفر :</h5>
              <h5>
                <span>{{ perPerson(provider.price) }}</span>
                <span> تومان </span>
              </h5>
            </div>
            <hr>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <h5>قیمت کل :</h5>
              <h5>
                <span>{{ totalPerson(provider.price) }}</span>
                <span> تومان </span>
              </h5>
            </div>
            <hr>
            <div class="">
              <a target="_blank" :href="provider.buy_link" class="btn btn-success w-100">نمایش در سایت</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "FlightComponent",
  data() {
    return {
      unique_id: `flight_${Math.floor(Math.random() * 999999999)}_${this.index}`,
      show: false
    }
  },
  methods: {
    perPerson(price) {
      return Number(price).toLocaleString()
    },
    totalPerson(price) {
      return Number(parseInt(price) * parseInt(this.adults)).toLocaleString()
    }
  },
  props: {
    data: Object,
    adults: String
  }
}
</script>

<style scoped>

</style>