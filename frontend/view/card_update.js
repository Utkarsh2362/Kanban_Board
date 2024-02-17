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
			        <input type="text" id="fname" name="firstname" placeholder="Enter the new title" v-model="card_title">
			      </div>
			      <div class="col-25">
			        <label for="fname"><h3>Content</h3></label>
			      </div>
			      <div class="col-75">
			        <input type="text" id="fname" name="firstname" placeholder="Add new description" v-model="content">
			      </div>
			      <div class="col-25">
			        <label for="fname"><h3>Completed</h3></label>
			      </div>
			      <div class="col-75">
			    <label class="switch">
				  <input type="checkbox" id="checkbox" v-model="checked">
				  
				  <span class="slider round"></span>
				</label>
					
			      </div>			      
			    </div> 


			    <div class="row">
			      <input type="button" value="Submit" @click="update_card">
			    </div>
			  </form>
			</div>


	`,


	data() {
		return {
			value: this.$route.params.value,
			checked: false,
			
			card_title: this.$route.params.value[2],
			content: this.$route.params.value[3],

			
		}
	},

	methods: {
		update_card() {

			CustomFetch(`http://localhost:5000/update_card/${this.value[0]}/${this.value[1]}/`, {
				method: 'PATCH',
				body: JSON.stringify({card_title: this.card_title, content: this.content, completed: this.checked}),
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("card updated successfully")
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert(err.message)
			})	
		}

	}
}