<template>
  <main class="container my-3">
    <!-- --- SEARCH --- -->
    <div class="row align-items-end">
      <!-- --- SOURCE --- -->
      <div class="col-12 col-xl-4">
        <div class="d-flex justify-content-between align-items-center">
          <label for="build_tour_source" class="text-muted">مقصد</label>
          <button class="btn btn-sm" v-if="body.target === 'GSM'" data-bs-toggle="modal"
                  data-bs-target="#alertTargetModal">
            <svg width="16" height="16"
                 fill="currentColor"
                 class="bi bi-exclamation-circle text-danger me-1" viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
              <path
                  d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
            </svg>
          </button>
        </div>
        <select name="build_tour_source" id="build_tour_source" class="form-select form-select-sm mt-2"
                v-model="body.target" v-on:change="getCalendarData">
          <option value="KIH">کیش</option>
          <option value="GSM">قشم</option>
        </select>
      </div>
      <!-- --- GO DATE DESKTOP --- -->
      <div class="d-none d-lg-block col-lg-3 mt-3 mt-lg-0">
        <div class="d-flex justify-content-between align-items-center"   @click="openBothDatePickers">
          <label for="date" class="text-muted mb-1">تاریخ</label>
        </div>
        <calender-index
          key="go_date"
          placeholder="تاریخ رفت"
          :show="show_datepicker_go"
          :disable-old="true"
          :days_data="calendar_data.go"
          @submitted="goDateSubmit"
          @showing="toggleDatePicker_go"
        />
      </div>
      <!-- --- BACK DATE DESKTOP --- -->
      <div class="d-none d-lg-block col-lg-3 mt-3 mt-lg-0">
        <div class="d-flex justify-content-between align-items-center" @click="openBothDatePickers">
          <label for="night_count" class="text-muted">تاریخ برگشت</label>
          <p class="m-0">
            <span>{{ body.night_count }}</span>
            <span class="me-1">شب</span>
          </p>
        </div>
        <calender-index
          key="back_date"
          placeholder="تاریخ برگشت"
          :show="show_datepicker_return"
          :disable-old="true"
          :days_data="calendar_data.return"
          @submitted="returnDateSubmit"
          @showing="toggleDatePicker_return"
        />
      </div>
      <!-- --- GO DATE MOBILE --- -->
      <div class="col-12 d-lg-none mt-3 mt-lg-0">
        <div class="d-flex justify-content-between align-items-center"   @click="openBothDatePickers">
          <label for="date" class="text-muted mb-1">تاریخ</label>
        </div>
        <calender-index
          key="go_date"
          placeholder="تاریخ رفت"
          :show="show_datepicker_go"
          :disable-old="true"
          :days_data="calendar_data.go"
          @submitted="goDateSubmit"
          @showing="toggleDatePicker_go"
        />
      </div>
      <!-- --- BACK DATE MOBILE --- -->
      <div class="col-12 d-lg-none mt-3 mt-lg-0">
        <div class="d-flex justify-content-between align-items-center" @click="openBothDatePickers">
          <label for="night_count" class="text-muted">تاریخ برگشت</label>
          <p class="m-0">
            <span>{{ body.night_count }}</span>
            <span class="me-1">شب</span>
          </p>
        </div>
        <calender-index
          key="back_date"
          placeholder="تاریخ برگشت"
          :show="show_datepicker_return"
          :disable-old="true"
          :days_data="calendar_data.return"
          @submitted="returnDateSubmit"
          @showing="toggleDatePicker_return"
        />
      </div>
      <!-- --- MODAL --- -->
      <div class="modal fade" id="alertTargetModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">ملاحظات</h1>
            </div>
            <div class="modal-body" style="line-height: 2">
              <p class="m-0 lh-2">برای تور دست ساز قشم٬ فقط روز های دوشنبه٬ سه شنبه٬ پنج شنبه و جمعه مجاز به جستجو
                میباشند.</p>
            </div>
          </div>
        </div>
      </div>
      <!-- --- SUBMIT --- -->
      <div class="col-12 col-lg-2 mt-3 mt-lg-0">
        <button class="btn btn-sm btn-success w-100" :disabled="loading" v-on:click="getData">جستجو</button>
      </div>
    </div>
    <hr>
    <!-- --- MAIN --- -->
    <section>
      <build-loading v-if="loading"></build-loading>
      <build-result v-if="show_result" :data="data" :adults="parseInt(this.body.adults)"
                    :target="body.target" :analysis_data="analyse_data" :analysis_loading="show_analyse_loading"></build-result>
    </section>
  </main>
</template>

<script>
import moment from "moment";
import moment_jalali from "moment-jalaali"; 
import BuildLoading from "@/components/BuildTour/BuildLoading";
import BuildResult from "@/components/BuildTour/BuildResult";
import {toast} from "vue3-toastify";
import CalenderIndex from "@/components/DatePicker/CalendarIndex";
import {router} from "@/routes";

export default {
  name: "BuildTourMain",
  components: {CalenderIndex, BuildResult, BuildLoading},
  data() {
    return {
      body: {
        "start_date": "",
        "end_date": "",
        "night_count": 0,
        "hotel_star": 5,
        "source": "MHD",
        "target": "KIH",
        "adults": 2,
        "status":true
      },
      calendar_data: {
        go: [],
        return: [],
      },
      show_datepicker: false,
      show_datepicker_go: false,
      show_datepicker_return: false,
      data: {},
      analyse_data: [],
      show_analyse_loading: false,
      loading: false,
      show_result: false,
      datepicker_min_date: "",
      minimum_date: ""
    }
  },
  methods: {
    openBothDatePickers() {
    this.show_datepicker_go = true;
    this.show_datepicker_return = true;
  },

    toggleDatePicker_go() {
    this.show_datepicker_go = !this.show_datepicker_go;
    if (this.show_datepicker_go){
      this.show_datepicker_return=true;
    }
    else{
      this.show_datepicker_go=true;
    }
    // this.show_datepicker_return = !this.show_datepicker_return;

    // this.show_datepicker_go=true;
    
    console.log("show_datepicker_go == "+this.show_datepicker_go);
    console.log("show_datepicker_return == "+this.show_datepicker_return);

  },
  toggleDatePicker_return() {
    this.show_datepicker_return = !this.show_datepicker_return;
    if (this.show_datepicker_return){
      this.show_datepicker_go = true;
    }
    else{
      this.show_datepicker_return=true;
    }
    
    // console.log("show_datepicker_go == "+this.show_datepicker_go);
    // console.log("show_datepicker_return == "+this.show_datepicker_return);

  },


  //   toggleDatePicker_go() {
  //     if (!this.show_datepicker_go){
  //       this.show_datepicker_go=true;
  //       this.show_datepicker_return=true;
  //     }
  //     // else{
  //     //   this.show_datepicker_go=false;
  //     //   this.show_datepicker_return=false;
  //     // }


  //   // this.show_datepicker_go = !this.show_datepicker_go;


  //   console.log("show_datepicker_go == "+this.show_datepicker_go);
  //   console.log("show_datepicker_return == "+this.show_datepicker_return);
  // },
  //   toggleDatePicker_return() {

  //     if (!this.show_datepicker_return){
  //       this.show_datepicker_go=true;
  //       this.show_datepicker_return=true;
  //     }
  //     // else{
  //     //   this.show_datepicker_go=false;
  //     //   this.show_datepicker_return=false;
  //     // }

  //   // this.show_datepicker_return = !this.show_datepicker_return;
  //   console.log("show_datepicker_go == "+this.show_datepicker_go);
  //   console.log("show_datepicker_return == "+this.show_datepicker_return);
  // },


    datePickerShowing(val) {

      // if (val){
      //   console.log("vaziiyat == "+val)
      //   this.show_datepicker_go=true;
      //   this.show_datepicker_return=true;
      // // this.show_datepicker=!this.show_datepicker;
      // }
      if (val) {
        this.show_datepicker = false;
        this.show_datepicker = val;
        console.log("vaziiyat == "+val)
        // this.show_datepicker_go=val;
        // this.show_datepicker_return=val;
      } 
      else {
        if (this.body.start_date.length > 2 && this.body.end_date.length > 2) {
          this.show_datepicker = false;
          
        }
      }
    },
    getCalendarData() {
      const body = {
        "source": this.body.source,
        "target": this.body.target,
        "skip_month": 0
      };
      this.calendar_data = {go: [], return: []}
      this.$http.post('/get-calendar/', body).then(r => {
        this.calendar_data = r.data;
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
      })
    },
    nextDay() {
      const today = moment(this.body.start_date, "YYYY-MM-DD");
      this.body.start_date = moment(today).add(1, 'd').format("YYYY-MM-DD")
    },
    prevDay() {
      const today = moment(this.body.start_date, "YYYY-MM-DD");
      this.body.start_date = moment(today).subtract(1, 'd').format("YYYY-MM-DD")
    },
    convertDate(date) {
      return moment_jalali(date).format("jYYYY/jMM/jDD");
    },
    getData() {
      //const gsm_valid_days = [1, 2, 4, 5];
      // if (this.body.target === "GSM" && !gsm_valid_days.includes(moment(this.body.start_date).day())) {

      //   toast.error("لطفا تاریخ معتبر وارد کنید", {
      //     autoClose: 6000,
      //     position: "bottom-left",
      //     rtl: false,
      //     closeOnClick: true
      //   });
      //   return false;
      // }
      if (!this.body.start_date || !this.body.end_date) {
        toast.error("لطفا تاریخ هارا وارد کنید", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      if (this.body.night_count < 0) {
        toast.error("تاریخ برگشت نمیتواند قبل از تاریخ رفت باشد", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      if (this.body.night_count < 3) {
        toast.error("تور شما نمیتواند کمتر از ۳ شب باشد", {
          autoClose: 6000,
          position: "bottom-left",
          rtl: false,
          closeOnClick: true
        });
        return false;
      }
      this.body.night_count = parseInt(this.body.night_count);
      this.$store.state.disable_header_link = true;
      this.loading = true;
      this.show_result = false;
      console.log("===================== Start Build Tour ========");
      this.$http.post('/build-tour/', this.body).then(res => {
        console.log(res);
        this.data = res.data;
        this.getAnalyseData();
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
      }).finally(() => {
        this.$store.state.disable_header_link = false;
        this.loading = false;
        this.show_result = true;
      })
    },
    getAnalyseData() {
      this.body.night_count = parseInt(this.body.night_count);
      this.show_analyse_loading = true;
      this.$store.state.disable_header_link = true;
      this.body.range = 7;
      this.$http.post('/build-tour-analyse/', this.body).then(res => {
        this.analyse_data = res.data;
      }).catch((e) => {
        if (e.response.status === 401) {
          return router.push('/login');
        }
      }).finally(() => {
      this.$store.state.disable_header_link = false;
        this.show_analyse_loading = false;
      })
    },
    calcNighCount() {
      if (!this.body.start_date || !this.body.end_date) {
        this.body.night_count = 0;
        return false;
      }
      let date_1 = new Date(this.body.start_date);
      let date_2 = new Date(this.body.end_date);
      let difference = date_1.getTime() - date_2.getTime();
      let total_days = Math.ceil(difference / (1000 * 3600 * 24));
      if (total_days < 0) {
        this.body.night_count = Math.abs(total_days);
      } else {
        this.body.night_count = total_days * -1;
      }
      return true
    },
    goDateSubmit(value) {
      const date = value.georgian;
      this.body.start_date = `${date.gy}-${date.gm < 9 ? '0' : ''}${date.gm}-${date.gd < 9 ? '0' : ''}${date.gd}`;
      this.calcNighCount();
      if (!value.data) {
        toast.warning("در این تاریخ پروازی وجود ندارد.", {
          autoClose: 6000,
          position: "top-left",
          rtl: false,
          closeOnClick: true
        });
      }
    },
    returnDateSubmit(value) {
      const date = value.georgian;
      this.body.end_date = `${date.gy}-${date.gm < 9 ? '0' : ''}${date.gm}-${date.gd < 9 ? '0' : ''}${date.gd}`;
      this.calcNighCount();
      if (!value.data) {
        toast.warning("در این تاریخ پروازی وجود ندارد.", {
          autoClose: 6000,
          position: "top-left",
          rtl: false,
          closeOnClick: true
        });
      }
    },
  },
  computed: {
    isValidDate() {
      return !moment(this.body.start_date, "YYYY-MM-DD").isAfter(new Date());
    },
    backDate() {
      return moment(this.body.start_date, "YYYY-MM-DD").add(this.body.night_count, 'd').format("YYYY-MM-DD");
    }
  },
  beforeUnmount() {
    this.$store.state.build_tour_data = this.$data;
  },
  created() {
    //
    // const data = this.$store.state.build_tour_data;
    // this.body = data.body;
    // this.data = {};
    // this.loading = data.loading;
    // this.show_result = data.show_result;
    // this.datepicker_min_date = data.datepicker_min_date;
    // this.minimum_date = data.minimum_date;
    //
    this.getCalendarData();
  },
}
</script>

<style scoped>

</style>