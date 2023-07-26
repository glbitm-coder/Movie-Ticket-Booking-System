<template>
  <div>
    <Home />

    <div class="theatres-container">
      <!-- Loop through each theatre -->
      <div v-for="theatre in theatres" :key="theatre.id" class="theatre-box">
        <h2>{{ theatre.name }}</h2>
        <div class="shows-container">
          <!-- Loop through each group of three shows in the theatre.shows array -->
          <div v-for="showGroup in chunkArray(theatre.shows, 3)" :key="showGroup[0].id" class="show-row">
            <!-- Display three shows in each row -->
            <div v-for="show in showGroup" :key="show.id" class="show-item">
              <!-- Display show details -->
              <div class="show-details">
                <p><strong>Show Name:</strong> {{ show.name }}</p>
                <p><strong>Date:</strong> {{ show.date }}</p>
                <p><strong>Tags:</strong> {{ show.tags }}</p>
                <p><strong>Price:</strong> {{ show.price }}</p>
                <b-btn class="success" v-if="theatre.bookings.length !== theatre.capacity" @click="openBookingModal(theatre)">Book</b-btn>
                <b-btn class="danger" v-else>Housefull</b-btn>
                <b-modal id="user-book-modal" v-model="showBookingModal" size="lg" variant="primary" no-close-on-backdrop>
                  <template #modal-header>
                    <h3 class="mb-0">Book</h3>
                  </template>
                  <template #default>
                    <div class="form-group">
                      <div id="user-book-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="user-book-error-message">
                          <ul>
                              <template v-if="errorMessages.length > 0">
                                <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                              </template>
                              <template v-else-if="serverErrorMessages.length > 0">
                                <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                              </template>
                          </ul>
                      </div>
                      <label for="available-seats">Available seats:</label>
                      <input type="text" id="available-seats" class="form-control" v-model="availableSeats" disabled/>
                    </div>
                    <div class="form-group">
                      <label for="number-of-tickets">Number of Tickets:</label>
                      <input type="number" id="number-of-tickets" class="form-control" v-model="numberOfTickets" />
                    </div>
                    <div class="form-group">
                      <label for="price">Price:</label>
                      <input type="text" id="price" class="form-control" v-model="show.price" disabled/>
                    </div>
                    <div class="form-group">
                      <label for="total_price">Total Price:</label>
                      <input type="text" id="total_price" class="form-control" v-model="totalPrice" disabled/>
                    </div>
                  </template>
                  <template #modal-footer>
                    <b-btn class="primary" @click="submitBooking">Confirm Booking</b-btn>
                    <b-btn @click="closeBookingModal">Close</b-btn>
                  </template>
                </b-modal>
                <!-- Add more show details as needed -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Home from './Home.vue'

export default {
  name: 'UserDashboard',
  components: {
    Home
  },
  data() {
    return {
      theatres: [],
      errorMessages: [],
      serverErrorMessages: [],
      isSubmitButtonClicked: false,
      showBookingModal: false,
      availableSeats: 0,
      numberOfTickets: 0,
      totalPrice: 0
    };
  },
  created() {
    this.fetchTheatres();
  },
  methods: {
    openBookingModal(theatre){
      this.showBookingModal = true;
      this.availableSeats = theatre.capacity - theatre.bookings.length;
    },
    closeBookingModal(){
      this.showBookingModal = false;
      
    },
    async fetchTheatres() {
      const user_id = parseInt(localStorage.getItem('userId'));
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre_api`, {
        method: 'GET',
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      });

      const data = await response.json();
      if (response.ok) {
        this.theatres = data.theatres;
      } else if (response.status === 409) {
        // Handle conflict
      } else {
        this.$store.commit('setNotification', {
          variant: 'error',
          message: 'Something went wrong. Try again!!!',
        });
      }
    },
    chunkArray(arr, size) {
      // Helper method to split the array into groups of given size
      const chunkedArr = [];
      for (let i = 0; i < arr.length; i += size) {
        chunkedArr.push(arr.slice(i, i + size));
      }
      return chunkedArr;
    },
  },
};
</script>

<style>
/* Add your custom styles here */
.theatres-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.theatre-box {
  width: 100%;
  margin: 10px;
  padding: 20px;
  border: 1px solid #ccc;
  background-color: yellow;
}

.shows-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  height: 245px;
  overflow-y: auto;
}

.show-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.show-item {
  width: calc(33.33% - 20px);
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: greenyellow;
}
.shows-scroll-wrapper {
  height: 300px; /* Set a fixed height for scrolling */
  overflow-y: auto; /* Enable vertical scrolling */
}
</style>