<template>
  <div class="c-position-relative ">
    <!-- --- INPUT --- -->
    <input type="text"
           :class="{'c-w-100 c-input': true, 'ltr-input': ltr_input}"
           v-on:keydown="disableTyping"
           v-on:click="show_box = !show_box"
           :placeholder="placeholder"
           v-model="input_text"
    >
    <!-- --- DATEPICKER BOX --- -->
    <div :class="{'c-datepicker-box-backdrop': true, 'd-none': !show_box}" v-on:click="show_box = false"></div>
    <div :class="{'c-position-absolute c-datepicker-box': true, 'c-datepicker-box-show': show_box}">
      <section class="c-box-main">
        <!-- --- DATEPICKER BOX TITLE --- -->
        <div class="c-box-title">
          <button class="c-box-title-btn" v-on:click="prevMonth">&lt;</button>
          <h5 class="m-0">
            <span>{{ getPersianMonthName(current_search.month) }}</span>
            <span class="mx-1">-</span>
            <span>{{ current_search.year }}</span>
          </h5>
          <button class="c-box-title-btn" v-on:click="nextMonth">&gt;</button>
        </div>
        <div class="c-grid">
          <!-- --- DATEPICKER DAYS TITLE --- -->
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">ش</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">ی</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">د</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">س</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">چ</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">پ</p>
            </div>
          </div>
          <div>
            <div class="c-button c-button-title">
              <p class="m-0 c-day">ج</p>
            </div>
          </div>
          <!-- --- DATEPICKER DAYS PREVIOUS DISABLE --- -->
          <div v-for="day in [...Array(prev_days_count).keys()]" :key="day">
            <div class="c-button disable"></div>
          </div>
          <!-- --- DATEPICKER DAYS --- -->
          <div v-for="day in [...Array(month_days_count).keys()]" :key="day">
            <div
                :class="{
                  'c-button': true, 
                  'active': isActiveDay(day + 1), 
                  'disable': isDisableDay(day + 1),
                  'lowest-price': isLowestPrice(day + 1)
                }"
                v-on:click="setDate(day + 1)">
              <div>
                <p class="m-0 c-day">{{ day + 1 }}</p>
                <span class="m-0 c-price">{{ getDayData(day + 1) }}</span>
              </div>
            </div>
          </div>
          <!-- --- DATEPICKER DAYS NEXT DISABLE --- -->
          <div v-for="day in [...Array(next_days_count).keys()]" :key="day">
            <div class="c-button disable"></div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import moment from "moment-jalaali";
import jalaali from 'jalaali-js';

export default {
  name: "CalenderIndex",
  // -----
  props: {
    show: {
      type: Boolean,
      required: false,
      default: false
    },
    placeholder: {
      type: String,
      required: false,
      default: "placeholder"
    },
    disableOld: {
      typ: Boolean,
      required: true,
      default: true
    },
    displayFormat: {
      type: String,
      required: false,
      default: "Y--M--D"
    },
    defaultDate: {
      type: Object,
      required: false,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: {
        year: 0,
        month: 0,
        day: 0
      }
    },
    days_data: {
      type: Array,
      required: false,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: []
    }
  }
  ,
// -----
  data() {
    return {
      show_box: this.show,
      min_date: {
        year: 0,
        month: 0,
        day: 0
      },
      select_date: this.defaultDate,
      current_search: {
        year: 0,
        month: 0
      },
      month_days_count: 0,
      prev_days_count: 0,
      next_days_count: 0,
      ltr_input: false,
      input_text: ""
    }
  }
  ,
// -----
  methods: {
    disableTyping(e) {
      e.preventDefault()
      return ""
    },
    convertPersianNumber(str) {
      var e = '۰'.charCodeAt(0);
      str = str.replace(/[۰-۹]/g, function (t) {
        return t.charCodeAt(0) - e;
      });

      e = '٠'.charCodeAt(0);
      str = str.replace(/[٠-٩]/g, function (t) {
        return t.charCodeAt(0) - e;
      });
      return str;
    }
    ,
    getPersianMonthName(month) {
      const months = {
        0: "فروردین",
        1: "اردیبهشت",
        2: "خرداد",
        3: "تیر",
        4: "مرداد",
        5: "شهریور",
        6: "مهر",
        7: "آبان",
        8: "آذر",
        9: "دی",
        10: "بهمن",
        11: "اسفند",
      }
      try {
        return months[month];
      } catch (e) {
        console.log('error in get persian month name', e);
        return "یافت نشد"
      }
    }
    ,
    nextMonth() {
      if (this.current_search.month < 11) {
        this.current_search.month += 1;
      } else {
        this.current_search.month = 0;
        this.current_search.year += 1;
      }
      this.calcMonthDays();
    }
    ,
    prevMonth() {
      if (this.disableOld) {
        if (this.current_search.year === this.min_date.year && this.current_search.month === this.min_date.month) {
          return false;
        }
      }
      if (this.current_search.month > 0) {
        this.current_search.month -= 1;
      } else {
        this.current_search.month = 11;
        this.current_search.year -= 1;
      }
      this.calcMonthDays();
    }
    ,
    calcPreDummyDays(day_of_week) {
      const days = {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 6,
        6: 0,
      }
      return days[day_of_week];
    }
    ,
    calcNextDummyDays(day_of_week) {
      const days = {
        0: 5,
        1: 4,
        2: 3,
        3: 2,
        4: 1,
        5: 0,
        6: 6,
      }
      return days[day_of_week];
    }
    ,
    calcMonthDays() {
      this.month_days_count = moment.jDaysInMonth(this.current_search.year, this.current_search.month);
      // calc previous days
      const pre_georgian_date_obj = jalaali.toGregorian(this.current_search.year, this.current_search.month + 1, 1);
      const pre_georgian_date = new Date(pre_georgian_date_obj.gy, pre_georgian_date_obj.gm - 1, pre_georgian_date_obj.gd);
      this.prev_days_count = this.calcPreDummyDays(pre_georgian_date.getDay());
      // calc next days
      const next_georgian_date_obj = jalaali.toGregorian(this.current_search.year, this.current_search.month + 1, this.month_days_count);
      const next_georgian_date = new Date(next_georgian_date_obj.gy, next_georgian_date_obj.gm - 1, next_georgian_date_obj.gd);
      this.next_days_count = this.calcNextDummyDays(next_georgian_date.getDay());
    }
    ,
    isActiveDay(day) {
      return this.select_date.year === this.current_search.year && this.select_date.month === this.current_search.month && this.select_date.day === day;
    }
    ,
    isDisableDay(day) {
      if (this.disableOld) {
        return this.current_search.year === this.min_date.year && this.current_search.month === this.min_date.month && day < this.min_date.day;
      }
      return false
    }
    ,
    setDate(day) {
      // check for disable day
      if (this.isDisableDay(day)) {
        return false;
      }
      //
      this.select_date.year = this.current_search.year;
      this.select_date.month = this.current_search.month;
      this.select_date.day = day;
      // this.show_box = false;
      const result = {
        "persian": {jy: this.select_date.year, jm: this.select_date.month + 1, jd: this.select_date.day},
        "georgian": jalaali.toGregorian(this.select_date.year, this.select_date.month + 1, this.select_date.day),
        "data": this.getDayData(day)
      }
      this.$emit("submitted", result);
      this.$emit('showing', false);
      this.input_text = this.getInputText();
      return true;
    },
    getDayData(day) {
      // check for disable day
      if (this.isDisableDay(day)) {
        return '';
      }
      const day_key = `${this.current_search.year}/${this.current_search.month + 1 < 10 ? '0' : ''}${this.current_search.month + 1}/${day < 10 ? '0' : ''}${day}`;
      const day_filter = this.days_data.filter(a => a.date === day_key);
      if (day_filter.length) {
        return Number(day_filter[0].price).toLocaleString();
      }
      return '';
    },

    getInputText() {
      try {
        if (this.select_date.year === 0 && this.select_date.month === 0 && this.select_date.day === 0) {
          return '';
        } else {
          switch (this.displayFormat) {
            case "jYYYY-jM-jD": {
              return `${this.select_date.year}-${this.select_date.month + 1}-${this.select_date.day}`
            }
            case "jYYYY/jM/jD": {
              return `${this.select_date.year}/${this.select_date.month + 1}/${this.select_date.day}`
            }
            case "YYYY-MM-DD": {
              const georgian_date = jalaali.toGregorian(this.select_date.year, this.select_date.month + 1, this.select_date.day);
              return `${georgian_date.gy}-${georgian_date.gm}-${georgian_date.gd}`;
            }
            case "YYYY/MM/DD": {
              const georgian_date = jalaali.toGregorian(this.select_date.year, this.select_date.month + 1, this.select_date.day);
              return `${georgian_date.gy}/${georgian_date.gm}/${georgian_date.gd}`;
            }
            case "Y--M--D": {
              return `${this.select_date.day} ${this.getPersianMonthName(this.select_date.month)} ${this.select_date.year}`;
            }
            default: {
              return `${this.select_date.day} ${this.getPersianMonthName(this.select_date.month)} ${this.select_date.year}`;
            }
          }
        }
      } catch (e) {
        return ''
      }
    },
    isLowestPrice(day) {
      if (this.isDisableDay(day)) return false;
      const day_key = `${this.current_search.year}/${this.current_search.month + 1 < 10 ? '0' : ''}${this.current_search.month + 1}/${day < 10 ? '0' : ''}${day}`;
      const day_filter = this.days_data.filter(a => a.date === day_key);
      if (!day_filter.length) return false;
      
      const currentPrice = Number(day_filter[0].price);
      const monthKey = `${this.current_search.year}/${this.current_search.month + 1 < 10 ? '0' : ''}${this.current_search.month + 1}`;
      const monthDays = this.days_data.filter(a => a.date.startsWith(monthKey));
      
      if (monthDays.length === 0) return false;
      
      const prices = monthDays.map(d => Number(d.price));
      const minPrice = Math.min(...prices);
      
      return currentPrice === minPrice;
    }
  },
// -----
  watch: {
    'show_box': function (val) {
      this.$emit('showing', val);
    },
    "show": function (val) {
      this.show_box = val;
    }
  },
// -----
  created: function () {
    // get date
    const now_georgian_date = new Date();
    const now_jalali_date = this.convertPersianNumber(new Intl.DateTimeFormat('fa-IR').format(now_georgian_date));
    const now_jalali_moment = moment(now_jalali_date, 'jYYYY/jM/jD');
    // set min date
    this.min_date.year = now_jalali_moment.jYear();
    this.min_date.month = now_jalali_moment.jMonth();
    this.min_date.day = now_jalali_moment.jDate();
    // set current search
    this.current_search.year = this.min_date.year;
    this.current_search.month = this.min_date.month;
    // set month days count
    this.calcMonthDays();
  }
}
</script>

<style scoped>
@import "../../assets/datepicker/main.css";

.lowest-price {
  background-color: #e8f5e9 !important;
  border: 2px solid #198754 !important;
  box-shadow: 0 0 5px rgba(25, 135, 84, 0.2) !important;
}

.lowest-price .c-day,
.lowest-price .c-price {
  color: #198754 !important;
  font-weight: 600 !important;
}

.lowest-price:hover {
  background-color: #d4edda !important;
  transform: scale(1.05);
  transition: all 0.2s ease;
}

.lowest-price.active {
  background-color: #198754 !important;
  color: white !important;
}

.lowest-price.active .c-day,
.lowest-price.active .c-price {
  color: white !important;
}
</style>
