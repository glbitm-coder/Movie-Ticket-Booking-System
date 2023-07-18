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
                    <div id="admin-theatre-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isSubmitButtonClicked" class="theatre-error-message">
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
                    <input type="text" id="place" class="form-control" v-model="theatre.place" />
                </div>
                <div class="form-group">
                    <label for="capacity">Capacity:</label>
                    <input type="number" id="capacity" class="form-control" v-model="theatre.capacity" />
                </div>
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="input_name" class="form-control" v-model="theatre.name" />
                </div>
                <div class="form-group">
                    <label for="image">Image:</label>
                    <!-- <input type="file" id="image" class="form-control-file" @change="handleImageUpload" /> -->
                    <img :src="theatre.image" />
                </div>
            </template>
            <template #modal-footer>
                <!-- <b-btn class="primary" @click="submitEditForm">Submit</b-btn> -->
                <b-btn @click="closeEditModal">Close</b-btn>
            </template>
        </b-modal>
    </div>
</template>

<script>

export default {
    name: 'AdminTheatre',
    props: {
        theatre: {
            type: Object,
            required: true
        }
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
            serverErrorMessages: []
        }
    },
    computed: {
        getImageUrl() {
  return (imagePath) => {
    imagePath = imagePath.replace('src/', '');
    return imagePath;
  };
},
    },
    methods: {
        handleImageUpload(event) {
            // Handle the image upload here
            theatre.image = event.target.files[0];
        },
        editTheatre(theatre) {
            // Set the data of the selected theatre to the editTheatreData property
            this.editTheatreData = {
                id: theatre.id,
                name: theatre.storedName,
                place: theatre.storedPlace,
                capacity: theatre.storedCapacity,
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
    },
}

</script>

<style>

</style>