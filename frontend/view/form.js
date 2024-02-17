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
			        <input type="text" id="fname" name="firstname" placeholder="Enter the title" v-model="form_info.title">
			      </div>
			    </div> <br>

			    <div class="row">
			      <input type="button" value="Submit" @click="create_list">
			    </div>
			  </form>
			</div>

          



	`,
	data(){
		return {
			form_info: {
				title : "",
			}

		}
	},

	methods: {
		create_list() {
			CustomFetch(`http://localhost:5000/add_list`, {
				method: 'POST',
				body: JSON.stringify(this.form_info),
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("list created successfully")
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert(err.message)
			})
		}
	}



}