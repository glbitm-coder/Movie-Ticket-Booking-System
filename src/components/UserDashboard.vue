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
                <b-btn class="success" v-if="isTheatreNotHousefull(theatre)" @click="openBookingModal(theatre, show)">Book</b-btn>
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
                      <input type="number" id="available-seats" class="form-control" v-model="availableSeats" disabled/>
                    </div>
                    <div class="form-group">
                      <label for="number-of-tickets">Number of Tickets:</label>
                      <input type="number" id="number-of-tickets" class="form-control" v-model="numberOfTickets" />
                    </div>
                    <div class="form-group">
                      <label for="price">Price:</label>
                      <input type="number" id="price" class="form-control" v-model="price" disabled/>
                    </div>
                    <div class="form-group">
                      <label for="total_price">Total Price:</label>
                      <input type="number" id="total_price" class="form-control" v-model="totalPrice" disabled/>
                    </div>
                  </template>
                  <template #modal-footer>
                    <b-btn class="primary" @click="submitBooking(theatre, show)">Confirm Booking</b-btn>
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
    <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/>
  </div>
</template>

<script>
import Home from './Home.vue'
import Notification from './Notification.vue'

export default {
  name: 'UserDashboard',
  components: {
    Home,Notification
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
      totalPrice: 0,
      price: 0,
      currentTheatre: null,
      currentShow: null,
    };
  },
  created() {
    this.fetchTheatres();
  },
  watch: {
    numberOfTickets: function(newValue) {
      // Calculate the total price by multiplying the number of tickets with the show price.
      this.totalPrice = newValue * this.price;
    }
  },
  methods: {
    clearNotification() {
            this.$store.commit('clearNotification');
        },
    openBookingModal(theatre, show){
      this.currentTheatre = theatre; // Store the current theatre
      this.currentShow = show; 
      this.showBookingModal = true;
      this.availableSeats = theatre.capacity;
      const bookedTickets = theatre.bookings.reduce((totalTickets, booking) => totalTickets + booking.number_of_tickets, 0);
      this.availableSeats -= bookedTickets;
      this.price = show.price;

    },
    closeBookingModal(){
      this.showBookingModal = false;
      this.availableSeats = 0;
      this.price = 0;
      
    },
    isTheatreNotHousefull(theatre){
      const bookedTickets = theatre.bookings.reduce((totalTickets, booking) => totalTickets + booking.number_of_tickets, 0);
      if(bookedTickets === theatre.capacity){
        return false;
      }
      return true;
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
    validation() {

      let message = 'Number of tickets cannot be 0 or empty'
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (this.numberOfTickets === null || this.numberOfTickets === 0 || this.numberOfTickets === "") {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (this.numberOfTickets === null || this.numberOfTickets === 0 || this.numberOfTickets === "") {
          this.errorMessages.push(message);
        }
      }


      message = 'Number of tickets cannot be more than available seats';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (this.numberOfTickets > this.availableSeats) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (this.numberOfTickets > this.availableSeats) {
          this.errorMessages.push(message);
        }
      }
    },
    async submitBooking(theatre, show){
      this.isSubmitButtonClicked = true;

      this.validation();
      if (this.errorMessages.length > 0) {
        return;
      }
      const user_id = parseInt(localStorage.getItem('userId'));
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${this.currentTheatre.id}/show/${this.currentShow.id}/booking_api`, {
        method: "POST",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          total_price: this.totalPrice,
          number_of_tickets: this.numberOfTickets
        })
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.$store.commit('setNotification', { variant: 'success', message: data.message });
          await this.fetchTheatres();
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
        this.closeBookingModal();
      })
    }
  },
};
</script>

<style scoped>
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
  border: 2px solid red;
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
  border: 4px solid blue;
  background-color: greenyellow;
}
#user-book-error-message {
  width: 750px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#user-book-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}

</style>