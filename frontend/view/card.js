import CustomFetch from '../CustomFetch.js'


export default {
	template: `

			<div class="form_class">
			  <form>
			        <div class="row">
			      <div class="col-25">
			        <label for="fname"><h3>Title</h3></label>
			      </div>
			      <div class="col-75">
			        <input type="text" id="fname" name="firstname" placeholder="Enter the title" v-model="form_info.card_title">
			      </div>
			      <div class="col-25">
			        <label for="fname"><h3>Content</h3></label>
			      </div>
			      <div class="col-75">
			        <input type="text" id="fname" name="firstname" placeholder="Add description" v-model="form_info.content">
			      </div>
			      <div class="col-25">
			        <label for="fname"><h3>Deadline</h3></label>
			      </div>
			      <div class="col-75">
			        <input type="date" id="fname" name="firstname" placeholder="Enter the dealine" v-model="form_info.deadline">
			      </div>			      			      
			    </div> <br>

			    <div class="row">
			      <input type="button" value="Submit" @click="create_card">
			    </div>
			  </form>
			</div>



	`,

	data(){
		return{
			new_value: this.$route.params.value,
            form_info: {
            	card_title: "",
            	content: "",
            	deadline: ""
            }
		}
	},

	methods: {
		create_card() {
			let [month, day, year] = this.form_info.deadline.split('/');

            let result = [year, month, day].join('-');
            this.form_info.deadline = result.slice(1, -1);
			CustomFetch(`http://localhost:5000/add_card/${this.new_value}/`, {
				method: 'POST',
				body: JSON.stringify(this.form_info),
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("card created successfully")
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert(err.message)
			})			
		}
	}
}