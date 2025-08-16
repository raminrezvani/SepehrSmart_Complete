<template>
  <section class="container py-3">
    <!-- --- SEARCH SECTION --- -->
    <div class="row align-items-end">
      <!-- --- ONE WAY --- -->
      <div class="col-12 mb-0 mb-md-3">
        <input type="radio" class="d-none" v-model="body.one_way" :value="true" name="flight_one_way"
               id="flight_one_way_true">
        <label for="flight_one_way_true" class="toggle_input_label right">یک طرفه</label>
        <input type="radio" class="d-none" v-model="body.one_way" :value="false" name="flight_one_way"
               id="flight_one_way_false">
        <label for="flight_one_way_false" class="toggle_input_label left">دو طرفه</label>
      </div>
      <!-- --- SOURCE --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="flight_source">مبدا</label>
        <select name="flight_source" id="flight_source" class="form-select" v-model="body.source">

          
          <option value="MHD">مشهد</option>
          <option value="THR">تهران</option>
          <option value="IFN">اصفهان</option>
          <option value="SYZ">شیراز</option>
          <option value="TBZ">تبریز</option>
          <option value="GSM">قشم</option>
          <option value="KIH">کیش</option>
          <option value="AZD">یزد</option>
          <option value="AWZ">اهواز</option>
          <option value="BND">بندرعباس</option>
          <option value="KER">کرمان</option>
          <option value="KSH">کرمانشاه</option>
          <option value="RAS">رشت</option>
          <option value="SRY">ساری</option>
          <option value="ZBR">چابهار</option>
           <!-- <option value="DXB">دبی</option>
          <option value="IST">استانبول</option>   -->

          <option value="ABD">آبادان</option>
          <option value="BUZ">بوشهر</option>
          <option value="GBT">گرگان</option>
          <option value="OMH">ارومیه</option>
          <option value="ADU">اردبیل</option>
          <option value="HDM">همدان</option>
          <option value="RZR">رامسر</option>
          <option value="KHD">خرم آباد</option>
          <!-- <option value="NSH">نوشهر</option> -->


          <!-- <option value="FRA">فرانکفورت</option>
          <option value="LON">لندن</option>
          <option value="YTO">تورنتو</option>
          <option value="IST">استانبول</option>
          <option value="DOH">دوجه</option> -->

        </select>
      </div>
      <!-- --- TARGET --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="flight_target">مقصد</label>
        <select name="flight_target" id="flight_target" class="form-select" v-model="body.target">




          
          <option value="MHD">مشهد</option>
          <option value="THR">تهران</option>
          <option value="IFN">اصفهان</option>
          <option value="SYZ">شیراز</option>
          <option value="TBZ">تبریز</option>
          <option value="GSM">قشم</option>
          <option value="KIH">کیش</option>
          <option value="AZD">یزد</option>
          <option value="AWZ">اهواز</option>
          <option value="BND">بندرعباس</option>
          <option value="KER">کرمان</option>
          <option value="KSH">کرمانشاه</option>
          <option value="RAS">رشت</option>
          <option value="SRY">ساری</option>
          <option value="ZBR">چابهار</option>
           <!-- <option value="DXB">دبی</option>
          <option value="IST">استانبول</option>   -->

          <option value="ABD">آبادان</option>
          <option value="BUZ">بوشهر</option>
          <option value="GBT">گرگان</option>
          <option value="OMH">ارومیه</option>
          <option value="ADU">اردبیل</option>
          <option value="HDM">همدان</option>
          <option value="RZR">رامسر</option>
          <option value="KHD">خرم آباد</option>
          <!-- <option value="NSH">نوشهر</option> -->


          <!-- <option value="DXB">دبی</option>
          <option value="LON">لندن</option>
          <option value="FRA">فرانکفورت</option>
          <option value="YTO">تورنتو</option>
          <option value="IST">استانبول</option>
          <option value="DOH">دوجه</option> -->
        </select>
      </div>
      <!-- --- START DATE --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="flight_start_date">تاریخ رفت</label>
        <date-picker id="date" class="mt-1 w-100 h-100" :min="datepicker_min_date" :popover="true"
                     v-model="body.start_date"></date-picker>
      </div>
      <!-- --- END DATE --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="flight_start_date">تاریخ برگشت</label>
        <date-picker id="date" class="mt-1 w-100 h-100" :min="body.start_date" :popover="true"
                     :disabled="true" v-if="body.one_way"></date-picker>
        <date-picker id="date" class="mt-1 w-100 h-100" :min="body.start_date" :popover="true"
                     v-model="body.end_date" :disabled="false" v-else></date-picker>
      </div>
      <!-- --- ADULT --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <label for="flight_search_adult">تعداد بزرگسال</label>
        <select id="flight_search_adult" class="form-select" v-model="adults">
          <option value="1">۱ بزرگسال</option>
          <option value="2">۲ بزرگسال</option>
          <option value="3">۳ بزرگسال</option>
          <option value="4">۴ بزرگسال</option>
        </select>
      </div>
      <!-- --- SUBMIT --- -->
      <div class="col-12 col-md-2 mt-3 mt-md-0">
        <button class="btn btn-success w-100" v-on:click="getData">جستجو</button>
      </div>
    </div>
    <!-- --- GRID --- -->
    <section>
      <flight-loading v-if="loading"></flight-loading>
      <flight-one-way :data="data" :adults="search_adults" v-if="show_result && body.one_way"></flight-one-way>
      <flight-two-way :data="data" :adults="search_adults" v-if="show_result && !body.one_way"></flight-two-way>
    </section>
  </section>
</template>

<script>
import FlightOneWay from "@/components/Flight/FlightOneWay";
import FlightTwoWay from "@/components/Flight/FlightTwoWay";

import {toast} from "vue3-toastify";
import FlightLoading from "@/components/Flight/FlightLoading";
import {router} from "@/routes";

export default {
  name: "FlightMain",
  components: {FlightLoading, FlightOneWay,FlightTwoWay},
  data() {
    return {
      datepicker_min_date: '',
      body: {
        source: "MHD",
        target: "KIH",
        start_date: "",
        end_date: "",
        one_way: true
      },
      adults: "1",
      search_adults: "1",
      data: [],
      loading: false,
      show_result: false
    }
  },
  methods: {
    showError(text) {
      return toast.error(text, {
        autoClose: 6000,
        position: "top-left",
        rtl: false,
        closeOnClick: true
      });
    },
    getData() {
      if (!this.body.source) {
        this.showError("لطفا مبدا را انتخاب کنید")
      } else if (!this.body.target) {
        this.showError("لطفا مقصد را انتخاب کنید")
      } else if (!this.body.start_date) {
        this.showError("لطفا تاریخ رفت را انتخاب کنید")
      } else if (!this.body.one_way && !this.body.end_date) {
        this.showError("لطفا تاریخ برگشت را انتخاب کنید")
      } else {
        if (this.body.one_way) {
          this.body.end_date = this.body.start_date;
        }
        this.loading = true;
        this.show_result = false;
        this.search_adults = this.adults;
        this.$http.post("get-flight/", this.body).then((res) => {
          this.data = res.data;
        }).catch((e) => {
          if (e.response.status === 401) {
            return router.push('/login');
          }
        }).finally(() => {
          this.loading = false;
          this.show_result = true;
        })
      }
    }
  },
  created() {
    function formatDate(date) {
      let d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2)
        month = '0' + month;
      if (day.length < 2)
        day = '0' + day;

      return [year, month, day].join('-');
    }

    this.datepicker_min_date = formatDate(new Date);
    this.body.start_date = this.datepicker_min_date;
  }
}
</script>

<style scoped>
.toggle_input_label {
  transition: all .3s;
  width: 100px;
  cursor: pointer;
  text-align: center;
  background: rgba(255, 193, 0, .35);
}

.toggle_input_label.right {
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

.toggle_input_label.left {
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}

input[name='flight_one_way']:checked + label {
  background: #FFC100 !important;
}

@media (max-width: 766px) {
  .toggle_input_label {
    width: 50%;
  }
}
</style>