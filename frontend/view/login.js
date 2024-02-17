import CustomFetch from '../CustomFetch.js'

export default {
	template: `

	          <div class="class_1">
				<div class="container">
				  <form>
				  	<h1>Login</h1>
				  	<div class="form-group">
				  	  <label for="username">Email:</label>	
				  	  <input type="text" name="email" class="form-control" required v-model="logininfo.email"/>
				    </div>
				    <div class="form-group">
				    	<label for="password">Password:</label>
				      <input type="password" name="password" class="form-control" required v-model="logininfo.password"/>
				    </div>
				    <button type="button" class="btn" @click="login">login</button>
				    
				  </form>
				</div>
				</div>



	`,
	data() {
		return{
		logininfo: {
		   email: "",
		   password: "",				
		}				
	  }
	},
	
	methods: {
		login() {
			CustomFetch(`http://localhost:5000/login?include_auth_token`, {
				method: 'POST',
				body: JSON.stringify(this.logininfo),
				headers: {
					'Content-Type': 'application/json'
				}

			})
			.then((data) => {
				localStorage.setItem('Authentication-Token', data.response.user['authentication_token'])
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert("Wrong email adress or password")
			})
		}

	}
}




