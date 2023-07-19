<template>
    <div>
        <div class="d-flex justify-content-between">
            <b-btn  variant="primary" @click="editTheatre(theatre)">Edit Theatre</b-btn>
            <b-btn variant="danger" @click="deleteTheatre(theatre)">Delete Theatre</b-btn>
        </div>
        <b-modal id="edit-admin-theatre-modal" v-model="showEditModal" size="lg" variant="primary" no-close-on-backdrop>
            <template #modal-header>
                <h3 class="mb-0">Edit Theatre</h3>
            </template>
            <template #default>
                <div class="form-group">
                    <div id="admin-theatre-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isEditSubmitButtonClicked" class="theatre-error-message">
                        <ul>
                            <template v-if="errorMessages.length > 0">
                                <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                            </template>
                            <template v-else-if="serverErrorMessages.length > 0">
                                <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                            </template>
                        </ul>
                    </div>
                    <label for="place">Edit Place:</label>
                    <input type="text" id="place" class="form-control" v-model="editTheatreData.place" />
                </div>
                <div class="form-group">
                    <label for="capacity">Edit Capacity:</label>
                    <input type="number" id="capacity" class="form-control" v-model="editTheatreData.capacity" />
                </div>
                <div class="form-group">
                    <label for="name">Edit Name:</label>
                    <input type="text" id="input_name" class="form-control" v-model="editTheatreData.name" />
                </div>
                <div class="form-group">
                    <label for="image">Image:</label>
                    <!-- <input type="file" id="image" class="form-control-file" @change="handleImageUpload" /> -->
                    <img :src="getImageUrl(theatre.image)" class="modal-image" />
                </div>
            </template>
            <template #modal-footer>
                <b-btn class="primary" @click="submitEditForm(theatre)">Submit</b-btn>
                <b-btn @click="closeEditModal">Close</b-btn>
            </template>
        </b-modal>
        <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/>
    </div>
</template>

<script>
import Notification from './Notification.vue'

export default {
    name: 'AdminTheatre',
    props: {
        theatre: {
            type: Object,
            required: true
        }
    },
    components:{
        Notification
    },
    data() {
        return {
            showEditModal: false,
            editTheatreData: {
                id: null,
                name: "",
                place: "",
                capacity: "",
                image: null
            },
            errorMessages: [],
            serverErrorMessages: [],
            isEditSubmitButtonClicked: false
        }
    },
    methods: {
        clearNotification() {
            this.$store.commit('clearNotification');
        },
        async fetchTheatre(theatre_id) {
            const response = await fetch(`http://127.0.0.1:5000/theatre_api/${theatre_id}`, {
                method: "GET",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                }
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    this.editTheatreData = data
                }
                else if (result.status === 409) {

                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
            })
        },
        getImageUrl(imagePath) {
            return require(`../assets/images/${imagePath}`)
        },
        editTheatre(theatre) {
            // Set the data of the selected theatre to the editTheatreData property
            this.editTheatreData = {
                id: theatre.id,
                name: theatre.name,
                place: theatre.place,
                capacity: theatre.capacity,
                image: null, // We don't update the image here, it will be updated later if changed
            };

            // Open the edit modal
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editTheatreData = {
                id: null,
                name: "",
                place: "",
                capacity: "",
                image: null,
            };
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
            this.validateEachEntity(this.editTheatreData.name, message);

            message = 'Place cannot be empty';
            this.validateEachEntity(this.editTheatreData.place, message);

            message = 'Capacity cannot be empty';
            this.validateEachEntity(this.editTheatreData.capacity, message);
        },
        async submitEditForm(theatre) {
            this.isEditSubmitButtonClicked = true;
            this.validation();
            if (this.errorMessages.length > 0) {
                return;
            }
            const formData = new FormData();

            if (this.editTheatreData.name !== theatre.name) {
                formData.append("input_name", this.editTheatreData.name);
            }
            if (this.editTheatreData.place !== theatre.place) {
                formData.append("input_place", this.editTheatreData.place);
            }
            if (this.editTheatreData.capacity !== theatre.capacity) {
                formData.append("input_capacity", this.editTheatreData.capacity);
            }

            if (formData.keys().next().done) {
                // No data in formData, so skip the API call
                this.closeEditModal();
                return;
            }
            const response = await fetch(`http://127.0.0.1:5000/theatre_api/${theatre.id}`, {
                method: "PUT",
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token'),
                },
                body: formData,
            }).then(async result => {
                const data = await result.json();
                if (result.ok) {
                    theatre.id = data.id;
                    theatre.name = data.name;
                    theatre.place = data.place;
                    theatre.capacity = data.capacity;
                    theatre.image = data.image;
                    this.$store.commit('setNotification', { variant: 'success', message: data.message });
                }
                else {
                    this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
                }
                this.closeEditModal();
            })
        }
    },
}

</script>

<style>

.modal-image {
  max-width: 100%;
  max-height: 400px; /* Adjust this value as needed to fit the image within the modal */
  margin: auto;
  display: block;
}

#admin-theatre-error-message {
  width: 750px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#admin-theatre-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}

</style>