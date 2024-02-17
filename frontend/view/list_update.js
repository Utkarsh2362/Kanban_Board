import CustomFetch from '../CustomFetch.js'


export default {
	template: `
         
            <div class="form_class">
			  <form>
			        <div class="row">
			      <div class="col-25">
			        <label for="fname"><h3>New Title</h3></label>
			      </div>
			      <div class="col-75">
			        <input type="text" id="fname" name="firstname" placeholder="Enter the new title" v-model="form_data.title">
			      </div>
			    </div> <br>
                   
			    <div class="row">
			      <input type="button" value="Submit" @click="update_list">
			    </div>
			  </form>
			</div>

          



	`,
	data(){
		return{
			value: this.$route.params.value,
			form_data: {
				title: ""
			}
		}
	},


	methods: {
		update_list() {
			if(this.form_data.title.trim().length != 0){
			CustomFetch(`http://localhost:5000/api/${this.value}/update/`, {
				method: 'PATCH',
				body: JSON.stringify(this.form_data),
				headers: {
					'Content-Type': 'application/json',
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("list title updated successfully")
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert(err.message)
			})
		
		}
		else{
			alert("Title required");
		}
	  }

	}
	



}

