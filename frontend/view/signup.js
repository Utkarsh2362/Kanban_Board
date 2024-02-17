import CustomFetch from '../CustomFetch.js'

export default {
	template: `
		        <div class="class_1">
					<div class="container">
					  <form>
					  	<h1>Signup</h1>
					  	<div class="form-group">
					  	  <label for="email">Email:</label>	
					  	  <input type="text" name="email" class="form-control" required v-model="signupinfo.email"/>
					    </div>
					  	<div class="form-group">
					  	  <label for="username">Username:</label>	
					  	  <input type="text" name="username" class="form-control" required v-model="signupinfo.username"/>
					    </div>				    
					    <div class="form-group">
					    	<label for="password">Password:</label>
					      <input type="password" name="password" class="form-control" required v-model="signupinfo.password"/>
					    </div>
					    <button type="button" class="btn" @click="signup">signup</button>
						
					  </form>
					</div>
					</div>  

	`,
	data() {
		return{
		signupinfo: {
		   email: "",
		   username: "",
		   password: "",			
		}				
	  }
	},
	
	methods: {
		signup() {
			CustomFetch(`http://localhost:5000/user`, {
				method: 'POST',
				body: JSON.stringify(this.signupinfo),
				headers: {
					'Content-Type': 'application/json'
				}

			})
			.then((data) => {
				alert("Your account has been created, login with your email and password")
				this.$router.push({path: '/'})
				
			})
			.catch((err) =>{
				alert("Wrong email adress or password")
			})
		}

	}
}	




