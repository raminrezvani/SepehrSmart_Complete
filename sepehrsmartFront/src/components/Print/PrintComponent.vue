<template>
  <div class="print-sec">
    <div class="d-flex justify-content-between align-items-center">
      <h4>جستجوی تور مشهد به کیش</h4>
      <h5>
        <span>{{start_date}}</span>
        <span> به </span>
        <span>{{end_date}}</span>
      </h5>
    </div>
    <table class="table table-bordered mt-3">
      <thead>
      <tr>
        <th scope="col">هتل</th>
        <th scope="col">اتاق</th>
        <th scope="col">اطلاعات رفت</th>
        <th scope="col">اطلاعات برگشت</th>
        <th scope="col">قیمت هر نفر</th>
        <th scope="col">قیمت کل</th>
        <th scope="col">تامین کننده</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(hotel, index) in data" :key="index">
        <td>{{ hotel.hotel_name }}</td>
        <td>{{ hotel.providers[0].room_name }}</td>
        <td>{{ hotel.providers[0].go_flight_airline }} - {{ hotel.providers[0].go_flight_arrive_time }}</td>
        <td>{{ hotel.providers[0].return_flight_airline }} - {{ hotel.providers[0].return_flight_arrive_time }}</td>
        <td>{{ pricePerPerson(hotel.price) }}</td>
        <td>{{ priceFilter(hotel.price) }}</td>
        <td>{{ hotel.providers[0].provider_name }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "PrintComponent",
  props: {
    data: Array,
    start_date: String,
    end_date: String,
    night_count: String
  },
  methods: {
    priceFilter(price) {
      return Number(price).toLocaleString();
    },
    pricePerPerson(price) {
      return Number(Math.round(price / 2)).toLocaleString();
    }
  }
}
</script>

<style scoped>
.print-sec {
  position: absolute;
  width: 100%;
  min-height: 100%;
  height: fit-content;
  overflow-y: auto;
  padding: 5px 2rem 2rem;
  top: 0;
  right: 0;
  z-index: 999;
  background: #fff;
}
</style>