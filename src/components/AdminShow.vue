<template>
  <div>
    <div id="shows-box">
      <!-- Loop through each show in the theatre.shows array -->
      <div v-for="show in theatre.shows" :key="show.id" id="show-item">
        <!-- Show details -->
        <div id="show-details">
          <!-- Add your show details content here -->
          <!-- For example, you can display show name, date, etc. -->
          <div id="each-detail">
            <div id="show-name" class="right-details">
            Show Name: {{ show.name }}
            </div>
            <div id="show-date" class="left-details">
              Date: {{ show.date }}
            </div>
          </div>
          <div id="each-detail">
            <div id="show-tags" class="right-details">
              Tags: {{ show.tags }}
            </div>
            <div id="show-price" class="left-details">
              Price: {{ show.price }}
            </div>
          </div>
        </div>
        <!-- Show Actions dropdown -->
        <div id="show-actions">
          <!-- Actions dropdown menu -->
          <b-dropdown  variant="info"  class="mr-2">
            <template #button-content>
              Actions
            </template>
            <b-dropdown-item @click="editShow(show)">Edit Show</b-dropdown-item>
            <b-dropdown-item @click="deleteShow(theatre, show)">Delete Show</b-dropdown-item>
          </b-dropdown>
        </div>
        <b-modal id="admin-edit-show-modal" v-model="showEditShowModal" size="lg" variant="primary" no-close-on-backdrop>
          <template #modal-header>
            <h3 class="mb-0">Edit Show</h3>
          </template>
          <template #default>
            <div class="form-group">
              <div id="admin-show-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isEditSubmitButtonClicked" class="admin-show-error-message">
                  <ul>
                      <template v-if="errorMessages.length > 0">
                        <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                      </template>
                      <template v-else-if="serverErrorMessages.length > 0">
                        <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                      </template>
                  </ul>
              </div>
              <label for="name">Name:</label>
              <input type="text" id="name" class="form-control" v-model="editShowData.name" />
            </div>
            <div class="form-group">
              <label for="price">Price:</label>
              <input type="number" id="price" class="form-control" v-model="editShowData.price" />
            </div>
            <div class="form-group">
              <label for="date">Date:</label>
              <input type="date" id="date" class="form-control" v-model="editShowData.date" />
            </div>
            <div class="form-group">
              <label for="startTime">Start Time:</label>
              <input type="time" id="startTime" class="form-control" v-model="editShowData.startTime" />
            </div>
            <div class="form-group">
              <label for="endTime">End Time:</label>
              <input type="time" id="endTime" class="form-control" v-model="editShowData.endTime" />
            </div>
            <div class="form-group">
              <label for="tags">Tags:</label>
              <select id="tags" class="form-control" v-model="editShowData.tags" multiple>
                <option value="drama">Drama</option>
                <option value="thriller">Thriller</option>
                <option value="action">Action</option>
                <option value="romance">Romance</option>
                <option value="comedy">Comedy</option>
                <option value="fiction">Fiction</option>
                <option value="sports">Sports</option>
                <option value="horror">Horror</option>
                <!-- Add more options as needed -->
              </select>
            </div>
          </template>
          <template #modal-footer>
            <b-btn class="primary" @click="submitEditShowForm(theatre, show)">Submit</b-btn>
            <b-btn @click="closeEditShowModal">Close</b-btn>
          </template>
        </b-modal>
      </div>
    </div>
    <div class="theatre-circle-container">
      <div class="theatre-circle" @click="openAddShowModal">
        <div class="theatre-plus-container">
          <div class="theatre-horizontal-plus"></div>
          <div class="theatre-vertical-plus"></div>
        </div>
      </div>
    </div>
    <b-modal id="add-show-circle-modal" v-model="showAddShowModal" size="lg" variant="primary" no-close-on-backdrop>
      <template #modal-header>
        <h3 class="mb-0">Add Show</h3>
      </template>
      <template #default>
        <div class="form-group">
          <div id="admin-show-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isAddSubmitButtonClicked" class="admin-show-error-message">
              <ul>
                  <template v-if="errorMessages.length > 0">
                    <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                  </template>
                  <template v-else-if="serverErrorMessages.length > 0">
                    <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                  </template>
              </ul>
          </div>
          <label for="name">Name:</label>
          <input type="text" id="name" class="form-control" v-model="addShowData.name" />
        </div>
        <div class="form-group">
          <label for="price">Price:</label>
          <input type="number" id="price" class="form-control" v-model="addShowData.price" />
        </div>
        <div class="form-group">
          <label for="date">Date:</label>
          <input type="date" id="date" class="form-control" v-model="addShowData.date" />
        </div>
        <div class="form-group">
          <label for="startTime">Start Time:</label>
          <input type="time" id="startTime" class="form-control" v-model="addShowData.startTime" />
        </div>
        <div class="form-group">
          <label for="endTime">End Time:</label>
          <input type="time" id="endTime" class="form-control" v-model="addShowData.endTime" />
        </div>
        <div class="form-group">
          <label for="tags">Tags:</label>
          <select id="tags" class="form-control" v-model="addShowData.tags" multiple>
            <option value="drama">Drama</option>
            <option value="thriller">Thriller</option>
            <option value="action">Action</option>
            <option value="romance">Romance</option>
            <option value="comedy">Comedy</option>
            <option value="fiction">Fiction</option>
            <option value="sports">Sports</option>
            <option value="horror">Horror</option>
            <!-- Add more options as needed -->
          </select>
        </div>
      </template>
      <template #modal-footer>
        <b-btn class="primary" @click="submitAddShowForm(theatre)">Submit</b-btn>
        <b-btn @click="closeAddShowModal">Close</b-btn>
      </template>
    </b-modal>
    <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/> 
  </div>
</template>

<script>
import Notification from './Notification.vue'

export default {
  name: 'AdminShow',
  props: {
    theatre: {
      type: Object,
      required: true
    }
  },
  components: {
    Notification
  },
  data() {
    return {
      showEditShowModal: false,
      showAddShowModal: false,
      addShowData: {
        id: null,
        name: "",
        price: null,
        rating: 0,
        date: null, 
        startTime: null, 
        endTime: null,
        tags: [],
      },
      editShowData: {
        id: null,
        name: "",
        price: null,
        rating: 0,
        date: null, 
        startTime: null, 
        endTime: null,
        tags: [],
      },
      errorMessages: [],
      serverErrorMessages: [],
      isAddSubmitButtonClicked: false,
      isEditSubmitButtonClicked: false
    }
  },
  methods: {
    clearNotification() {
      this.$store.commit('clearNotification');
    },
    openAddShowModal() {
      this.showAddShowModal = true;
    },
    closeAddShowModal() {
      this.showAddShowModal = false;
      this.addShowData = {
        id: null,
        name: "",
        price: null,
        rating: 0,
        date: null, 
        startTime: null, 
        endTime: null,
        tags: []
      }
    },
    editShow(show){
      this.showEditShowModal = true;
      this.editShowData = {
          id: show.id,
          name: show.name,
          price: show.price,
          rating: show.rating,
          date: show.date, 
          startTime: show.startTime, 
          endTime: show.endTime,
          tags: show.tags.split(',')
      };
    },
    closeEditShowModal(){
      this.showEditShowModal = false;
      this.editShowData = {
        id: null,
        name: "",
        price: null,
        rating: 0,
        date: null, 
        startTime: null, 
        endTime: null,
        tags: []
      }
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
    validation(entity) {
      let message = 'Name cannot be empty'
      this.validateEachEntity(entity.name, message);

      message = 'Price cannot be empty';
      this.validateEachEntity(entity.price, message);

      message = 'Date cannot be empty';
      this.validateEachEntity(entity.date, message);

      const currentDate = new Date();
      const selectedDate = new Date(entity.date);
      message = 'Selected date cannot be in the past';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (entity.date != null && selectedDate.getDate() < currentDate.getDate()) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (entity.date != null && selectedDate.getDate() < currentDate.getDate()) {
          this.errorMessages.push(message);
        }
      }


      // Start time and End time validation
      message = 'Start time cannot be empty';
      this.validateEachEntity(entity.startTime, message);

      message = 'End time cannot be empty';
      this.validateEachEntity(entity.endTime, message);

      const selectedStartTime = new Date();
      if (entity.startTime != null) {
        selectedStartTime.setHours(Number(entity.startTime.slice(0, 2)));
        selectedStartTime.setMinutes(Number(entity.startTime.slice(3)));
      }

      const selectedEndTime = new Date();
      if (entity.endTime != null) {
        selectedEndTime.setHours(Number(entity.endTime.slice(0, 2)));
        selectedEndTime.setMinutes(Number(entity.endTime.slice(3)));
      }

      message = 'Start time cannot be before or equal to the current time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (entity.startTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
      }
      else {
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (entity.startTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.push(message);
          }
        }
      }

      message = 'End time cannot be before or equal to the current time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (entity.endTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
      }
      else {
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (entity.endTime != null && selectedEndTime <= currentTime) {
            this.errorMessages.push(message);
          }
        }
      }

      message = 'End time should be greater than start time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (entity.endTime != null && entity.startTime != null && selectedEndTime <= selectedStartTime) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }

      }
      else {
        if (entity.endTime != null && entity.startTime != null && selectedEndTime <= selectedStartTime) {
          this.errorMessages.push(message);

        }
      }

      // Tags validation
      message = 'No tags selected';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (entity.tags.length === 0) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }

      }
      else {
        if (entity.tags.length === 0) {
          this.errorMessages.push(message);

        }
      }
    },
    async submitAddShowForm(theatre) {
      this.isAddSubmitButtonClicked = true;
      this.validation(this.addShowData);
      if (this.errorMessages.length > 0) {
        return;
      }
      
      const user_id = parseInt(localStorage.getItem('userId')); 
      const tagsString = this.addShowData.tags.join(",");
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${theatre.id}/show_api`, {
        method: "POST",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input_name: this.addShowData.name,
          input_price: this.addShowData.price,
          input_date: this.addShowData.date,
          input_startTime: this.addShowData.startTime,
          input_endTime: this.addShowData.endTime,
          input_tags: tagsString
        })
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.$store.commit('setNotification', { variant: 'success', message: data.message });
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
        this.closeAddShowModal();
      })
    },
    async submitEditShowForm(theatre, show){
      this.isEditSubmitButtonClicked = true;
      this.validation(this.editShowData);
      if (this.errorMessages.length > 0) {
        return;
      }

      if (this.editShowData.name === show.name && this.editShowData.price === show.price && this.editShowData.date === show.date
      && this.editShowData.startTime === show.startTime && this.editShowData.endTime === show.endTime && this.editShowData.tags.join(",") === show.tags) {
        this.$store.commit('setNotification', { variant: 'info', message: 'No changes detected!' });
        this.closeEditShowModal();
        return;
      }

      const user_id = parseInt(localStorage.getItem('userId')); 
      const tagsString = this.editShowData.tags.join(",");
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${theatre.id}/show_api/${show.id}`, {
        method: "PUT",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input_name: this.editShowData.name,
          input_price: this.editShowData.price,
          input_date: this.editShowData.date,
          input_startTime: this.editShowData.startTime,
          input_endTime: this.editShowData.endTime,
          input_tags: tagsString
        })
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.$store.commit('setNotification', { variant: 'success', message: data.message });
          show.name = this.editShowData.name;
          show.price = this.editShowData.price;
          show.date = this.editShowData.date;
          show.startTime = this.editShowData.startTime;
          show.endTime = this.editShowData.endTime;
          show.tags = this.editShowData.tags.join(",");
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
        this.closeEditShowModal();
      })
    },
    async deleteShow(theatre, show){
      const confirmDelete = window.confirm('Are you sure you want to delete this theatre?');
      if (confirmDelete) {
        const user_id = parseInt(localStorage.getItem('userId')); 
        const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${theatre.id}/show_api/${show.id}`, {
                    method: "DELETE",
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                    },
                }).then(async result => {
                    const data = await result.json();
                    if (result.ok) {
                        this.$store.commit('setNotification', { variant: 'success', message: data.message });
                        theatre.shows = theatre.shows.filter((s) => s.id !== show.id);
                    }
                    else {
                        this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                    }
                })
      }
    }
  }
}

</script>

<style scoped>
.theatre-circle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40%;
}

.theatre-circle, .show-circle {
  position: relative;
  width: 100px;
  height: 100px;
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

#admin-show-error-message {
  width: 750px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#admin-show-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}
#shows-box {
    max-height: 235px; 
    overflow-y: auto; 
    margin-bottom: 10px;
  }

  #show-item {
    width: 100%;
    border: 1px solid #ccc;
    margin-bottom: 10px;
    background-color: lightcoral;
  }

  #show-actions {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
    margin-top: 10px;
  }

  #actions-message {
    text-align: center;
    /* Add other styling properties as needed */
  }
  #each-detail {
    display: flex;
    justify-content: space-between;
  }
  #show-actions .dropdown-button-color .dropdown-toggle{
    background-color: lightskyblue;
  }
  .left-details {
    padding-right: 10px;
  }

  .right-details {
    padding-left: 10px;
  }

</style>