<template>
  <div>
    <Home/>
    <div class="theatre-circle-container">
      <div class="theatre-circle" @click="openModal">
        <div class="theatre-plus-container">
          <div class="theatre-horizontal-plus"></div>
          <div class="theatre-vertical-plus"></div>
        </div>
      </div>
    </div>

    <b-modal id="circle-modal" v-model="showModal" size="lg" variant="primary" no-close-on-backdrop>
      <template #modal-header>
        <h3 class="mb-0">Add Theatre</h3>
      </template>
      <template #default>
        <div class="form-group">
          <div id="theatre-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="theatre-error-message">
              <ul>
                  <template v-if="errorMessages.length > 0">
                    <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                  </template>
                  <template v-else-if="serverErrorMessages.length > 0">
                    <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                  </template>
              </ul>
          </div>
          <label for="place">Place:</label>
          <input type="text" id="place" class="form-control" v-model="place" />
        </div>
        <div class="form-group">
          <label for="capacity">Capacity:</label>
          <input type="number" id="capacity" class="form-control" v-model="capacity" />
        </div>
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="input_name" class="form-control" v-model="name" />
        </div>
        <div class="form-group">
          <label for="image">Image:</label>
          <input type="file" id="image" class="form-control-file" @change="handleImageUpload" />
        </div>
      </template>
      <template #modal-footer>
        <b-btn class="primary" @click="submitForm">Submit</b-btn>
        <b-btn @click="closeModal">Close</b-btn>
      </template>
    </b-modal>
    <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/>


    <div>
      <div class="row mb-4" v-for="(row, index) in rows" :key="index">
        <div class="col-4" v-for="theatre in row" :key="theatre.id">
          <b-card :header="theatre.name" header-tag="header" bg-variant="secondary" text-variant="white">
            <b-card-text>
              <AdminShow :theatre="theatre" />
              <AdminTheatre :theatre="theatre" @theatre-deleted="removeTheatre"/>
            </b-card-text>
            <template #footer>
              <small class="text-muted">Last updated 3 mins ago</small>
            </template>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Home from './Home.vue'
import AdminShow from './AdminShow.vue'
import AdminTheatre from './AdminTheatre.vue'
import Notification from './Notification.vue'
export default {
  name: 'AdminDashboard',
  components: {
    Home, AdminShow, AdminTheatre,Notification
  },
  data() {
    return {
      showModal: false,
      name: "",
      place: "",
      capacity: "",
      image: "",
      errorMessages: [],
      serverErrorMessages: [],
      isSubmitButtonClicked: false,
      notification: null,
      theatres: [],
      cardsPerRow: 3
    }
  },
  mounted() {
    this.fetchTheatres();
    document.addEventListener('click', this.redirectIfTokenExpired);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.redirectIfTokenExpired);
  },
  computed: {
    rows() {
      // Slice the theatres array into chunks based on cardsPerRow
      return this.chunkArray(this.theatres, this.cardsPerRow);
    }
  },
  watch: {
    place(value) {
      this.handleInputChange('Place', value);
      this.serverErrorMessages = []
    },

    name(value) {
      this.handleInputChange('Name', value);
      this.serverErrorMessages = []

    },

    capacity(value) {
      this.handleInputChange('Capacity', value);
      this.serverErrorMessages = []
    }
  },
  methods: {
    clearNotification() {
            this.$store.commit('clearNotification');
        },
        removeTheatre(theatreId) {
      this.theatres = this.theatres.filter(theatre => theatre.id !== theatreId);
    },
    getColClass(theatresCount) {
      const colSize = Math.floor(12 / theatresCount);
      return `col-${colSize}`;
    },
    chunkArray(array, size) {
      // Helper function to split an array into chunks of given size
      const result = [];
      for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
      }
      return result;
    },
    clearNotification() {
      this.$store.commit('clearNotification');
    },
    isTokenExpired(expiryTime, isAuthenticated) {
      if (isAuthenticated) {
        if (expiryTime) {
          return Date.now() > new Date(expiryTime);
        } else {
          return true;
        }
      }
      return false;
    },
    redirectIfTokenExpired() {
      const expiryTime = this.$store.state.expiryTime;
      const isAuthenticated = this.$store.state.isAuthenticated;
      if (this.isTokenExpired(expiryTime, isAuthenticated)) {
        // Token has expired, redirect to home page
        this.$store.commit('setAuthentication', {
          isAuthenticated: false
        });
        this.$store.commit('setToken', {
          access_token: null
        });
        this.$store.commit('setExpiryTime', {
          expiryTime: null
        });
        this.$store.commit('setNotification', {
          variant: 'error',
          message: 'Your session is expired. Login again!!'
        });
        this.$router.push('/');
      }
    },
    handleInputChange(fieldName, fieldValue) {
      let message = '';
      message = fieldName + ' cannot be empty';
      this.validateEachEntity(fieldValue, message);
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.errorMessages = [];
      this.serverErrorMessages = [];
      this.showModal = false;
      this.isSubmitButtonClicked = false;
    },
    handleImageUpload(event) {
      // Handle the image upload here
      this.image = event.target.files[0];
    },
    validateEachEntity(entityToValidate, message) {
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (entityToValidate == null || entityToValidate == '') {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (entityToValidate == null || entityToValidate == '') {
          this.errorMessages.push(message);
        }
      }
    },
    validation() {

      let message = 'Name cannot be empty'
      this.validateEachEntity(this.name, message);

      message = 'Place cannot be empty';
      this.validateEachEntity(this.place, message);

      message = 'Capacity cannot be empty';
      this.validateEachEntity(this.capacity, message);

      message = 'Image cannot be empty';
      this.validateEachEntity(this.image, message);

      message = 'Invalid image file format. Please select a valid image file';
      const allowedExtensions = ["jpg", "jpeg", "png", "gif"];
      console.log(this.image.name);
      const fileExtension = this.image.name.split(".").pop().toLowerCase();
      if (this.errorMessages.includes(message)) {
        if (allowedExtensions.includes(fileExtension)) {
          this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        }
      }
      else {
        if (!allowedExtensions.includes(fileExtension)) {
          this.errorMessages.push(message);
        }
      }
    },
    async submitForm() {
      this.isSubmitButtonClicked = true;
      this.validation();
      if (this.errorMessages.length > 0) {
        return;
      }

      // Create a FormData object
      const formData = new FormData();
      formData.append('input_name', this.name);
      console.log(this.name);
      formData.append('input_place', this.place);
      formData.append('input_capacity', this.capacity);
      formData.append('input_image', this.image);
      const user_id = parseInt(localStorage.getItem('userId'));

      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre_api`, {
        method: "POST",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: formData,
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.$store.commit('setNotification', { variant: 'success', message: data.message });
          this.fetchTheatres();
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
        this.closeModal();
      })
    },
    async fetchTheatres() {

      const user_id = parseInt(localStorage.getItem('userId'));
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre_api`, {
        method: "GET",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        }
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.theatres = data.theatres
        }
        else if (result.status === 409) {

        }
        else {
          if(!data.error_messages.includes("There are no theatres"))
            this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
      })
    }
  }
}
</script>

<style scoped>
.theatre-circle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 80px);
}

.theatre-circle, .show-circle {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: rgb(44, 108, 128);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.theatre-plus-container, .show-plus-container {
  position: relative;
  width: 60%;
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.theatre-horizontal-plus,
.theatre-vertical-plus {
  position: absolute;
  background-color: #FFFFFF;
}

.theatre-horizontal-plus {
  width: 50%;
  height: 2px;
  top: 50%;
  transform: translateY(-50%);
}

.theatre-vertical-plus {
  width: 2px;
  height: 50%;
  left: 50%;
  transform: translateX(-50%);
}
#theatre-error-message {
  width: 750px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#theatre-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}


</style>

  