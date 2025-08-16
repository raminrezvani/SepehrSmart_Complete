<template>
    <div class="row mt-3">
      <!-- --- FILTER --- -->
      <div class="col-12 col-md-3">
        <div class="sticky-top">
          <div class="row align-items-center bg-white py-3 rounded">
            <!-- --- NAME --- -->
            <div class="col-12">
              <label for="filter_name" class="text-muted mb-1">ایرلاین</label>
              <!--          <input type="text" class="form-control" placeholder="نام هتل ..." v-model="filter_name" id="filter_name">-->
              <v-select multiple :options="['ماهان', 'وارش', 'کاسپین', 'ایران ایر تور']"></v-select>
            </div>
            <!-- --- SORT --- -->
            <div class="col-12 mt-3">
              <label for="order_by_filter" class="text-muted mb-1">مرتب سازی</label>
              <select class="form-select" id="order_by_filter">
                <option value="price_a">قیمت - کم به زیاد</option>
                <option value="price_d">قیمت - زیاد به کم</option>
                <option value="hour_d_a">ساعت پرواز - صبح به شب</option>
                <option value="hour_d_d">ساعت پرواز - شب به صبح</option>
              </select>
            </div>
            <!-- --- ANALYSIS --- -->
            <div class="col-12 mt-3">
              <div class="row">
                <div class="col-6">
                  <button class="btn btn-secondary w-100">
                    <svg width="23" height="23" fill="currentColor" class="bi bi-printer"
                         viewBox="0 0 16 16">
                      <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
                      <path
                          d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
                    </svg>
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-warning w-100" data-bs-toggle="modal"
                          data-bs-target="#alertCustomModal">ملاحظات
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-primary w-100 mt-3">
                    <!--                    <i class="fa fa-spinner fa-spin"></i>-->
                    آنالیز پروازی
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-info w-100 mt-3">
                    <!--                    <i class="fa fa-spinner fa-spin"></i>-->
                    بررسی ایرلاینی
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="row mt-3 bg-white rounded p-3 align-items-center">
            <div class="col-6">
              <p class="m-0">آخرین بروزرسانی : </p>
            </div>
            <div class="col-5">
              <p class="m-0">۱ دقیقه پیش</p>
            </div>
            <div class="col-1 text-danger">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                   class="bi bi-exclamation-circle" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                <path
                    d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
      <!-- --- RESULT --- -->
      <div class="col-12 col-md-9 mt-3 mt-md-0">
        <div class="alert alert-warning text-center" v-if="getSortedData.length === 0">
          <h5 class="m-0">پروازی یافت نشد</h5>
        </div>
        <!-- <flight-component v-for="(flight, index) in getSortedData" :key="index" :data="flight"
                          :adults="adults" v-else></flight-component> -->

            <!-- <flight-component-two-way v-for="(flight, index) in getSortedData" :key="index" :flight_go="flight_go" :flight_return="flight_return"
            :adults="adults" v-else></flight-component-two-way> -->
        <!-- <flight-component-two-way v-for="(flight, index) in getSortedData" :key="index" :data="flight" :returndata="flight_return"
            :adults="adults" v-else></flight-component-two-way> -->


        <flight-component-two-way 
            v-for="(flight, index) in getSortedData" 
            :key="index" 
            :data="flight.go_flight" 
            :returndata="flight.return_flight" 
            :adults="adults">
        </flight-component-two-way>

      </div>
    </div>
  </template>
  
  <script>
  import FlightComponentTwoWay from "@/components/Flight/FlightComponentTwoWay";
  
  export default {
    name: "FlightTwoWay",
    components: {FlightComponentTwoWay},
    props: {
      data: Array,
      returndata:Object,
      adults: String
    },
    computed: {


// bayad go_flight va return_flight baham tarkib shavand!!! (JOIN)
getSortedData() {
  let result = [];

  // Process go_flight
  for (let flight_go of this.data.go_flight) {
    let goProviders = flight_go.providers
      .filter(prv => parseInt(prv.seat) >= parseInt(this.adults))
      .sort((a, b) => a.price - b.price);

    if (goProviders.length) {
      flight_go.price = goProviders[0].price; // Set the lowest price for go_flight
      flight_go.providers = goProviders;

      // For each valid go_flight, iterate through return_flight
      for (let flight_return of this.data.return_flight) {
        let returnProviders = flight_return.providers
          .filter(prv => parseInt(prv.seat) >= parseInt(this.adults))
          .sort((a, b) => a.price - b.price);

        if (returnProviders.length) {
          flight_return.price = returnProviders[0].price; // Set the lowest price for return_flight
          flight_return.providers = returnProviders;

          // Push combined flight object into result
          result.push({
            go_flight: flight_go,
            return_flight: flight_return,
            total_price: flight_go.price + flight_return.price // Calculate total price
          });
        }
      }
    }
  }

  // Sort the result based on total price (go_flight + return_flight)
  result.sort((a, b) => a.total_price - b.total_price);

  // Print the final result to the console
  console.log("Final sorted result:", result);

  return result;
}



//         getSortedData() {
//   let result = [];

// //   // Ensure this.data.go_flight and this.data.return_flight are arrays
// //   if (!Array.isArray(this.data.go_flight) || !Array.isArray(this.data.return_flight)) {
// //     console.error('Invalid data format: Expected go_flight and return_flight to be arrays');
// //     return result;
// //   }

//   // Process go_flight
//   for (let flight_go of this.data.go_flight) {
//     let goProviders = flight_go.providers
//       .filter(prv => parseInt(prv.seat) >= parseInt(this.adults))
//       .sort((a, b) => a.price - b.price);

//     if (goProviders.length) {
//       flight_go.price = goProviders[0].price;
//       flight_go.providers = goProviders;

//       result.push({
//         go_flight: flight_go, // Store go_flight in result
//         return_flight: null   // Placeholder for return_flight (will add it later)
//       });
//     }
//   }

//   // Process return_flight (could be different from go_flight)
//   for (let flight_return of this.data.return_flight) {
//     let returnProviders = flight_return.providers
//       .filter(prv => parseInt(prv.seat) >= parseInt(this.adults))
//       .sort((a, b) => a.price - b.price);

//     if (returnProviders.length) {
//       flight_return.price = returnProviders[0].price;
//       flight_return.providers = returnProviders;

//       // Push each return flight separately, pairing with go_flight later if needed
//       result.push({
//         go_flight: null,        // Placeholder for go_flight (already processed)
//         return_flight: flight_return
//       });
//     }
//   }

//   // Sort the result based on price of go_flight or return_flight (depending on availability)
//   result.sort((a, b) => {
//     if (a.go_flight && b.go_flight) {
//       return a.go_flight.price - b.go_flight.price;
//     } else if (a.return_flight && b.return_flight) {
//       return a.return_flight.price - b.return_flight.price;
//     }
//     return 0;
//   });
//   console.log ("Final Sorted retuls  ",result);

//   return result;
// }


// OLD
    //   getSortedData() {
    //     let result = [];
       
    //     // for (let flight_go of this.data.go_flight) {
    //     //   let providers = flight_go.providers.filter(prv => parseInt(prv.seat) >= parseInt(this.adults)).sort((a, b) => a.price - b.price);
    //     //   if (providers.length) {
    //     //     flight_go.price = providers[0].price;
    //     //     flight_go.providers = providers;
    //     //     result.push(flight_go);
    //     //   }
    //     // }

    //     for (let flight of this.data) {
    //       let providers = flight.go_flight.providers.filter(prv => parseInt(prv.seat) >= parseInt(this.adults)).sort((a, b) => a.price - b.price);
    //       if (providers.length) {
    //         flight.go_flight.price = providers[0].price;
    //         flight.go_flight.providers = providers;
    //         result.push(flight);
    //       }
    //     }


    // //     let result_return = [];
       
    // //    for (let flight_return of this.data.return_flight) {
    // //      let providers = flight_return.providers.filter(prv => parseInt(prv.seat) >= parseInt(this.adults)).sort((a, b) => a.price - b.price);
    // //      if (providers.length) {
    // //         flight_return.price = providers[0].price;
    // //         flight_return.providers = providers;
    // //        result_return.push(flight_return);
    // //      }
    // //    }


    //     // for (let flight_return of this.data.return_flight) {
    //     //   let providers = flight_return.providers.filter(prv => parseInt(prv.seat) >= parseInt(this.adults)).sort((a, b) => a.price - b.price);
    //     //   if (providers.length) {
    //     //     flight_return.price = providers[0].price;
    //     //     flight_return.providers = providers;
    //     //     result.push(flight_return);
    //     //   }
    //     // }

    //     console.log(result);
    //     console.log(this.data.go_flight);
    //     // console.log("chetoriiiii");
    //     return result.sort((a, b) => a.price - b.price);
    //   }


    }
  }
  </script>
  
  <style scoped>
  
  </style>