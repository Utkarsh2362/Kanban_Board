import CustomFetch from '../CustomFetch.js'

export default {
	template: `

<div id="app">
  <header class="masthead clear">
    <div class="centered">
      <div class="site-branding">
        <h1 class="site-title">YOUR LISTS</h1> 
      </div>
    </div>
  </header>
  <button type="button" class="btn btn-danger" @click="logout">Sign Out</button> <button type="button" class="btn btn-success" @click="summary_view" >Summary</button> <button type="button" class="btn btn-primary" @click="list_download" >Export</button><br><br>
  <main class="main-area">
    <div class="centered">
      <section class="cards">
        <article v-for="(list, index) in lists" class="card">
          

            <div class="card-content">
          <div>
			  <b-dropdown id="dropdown-1" text= "Action" variant="outline-danger" class="m-md-2">
			    <b-dropdown-item @click="edittitle(index)">Edit Title</b-dropdown-item>
			    <b-dropdown-item @click="deletelists(index)">Delete List</b-dropdown-item>
			    <b-dropdown-divider></b-dropdown-divider>
			    <b-dropdown-item active>Active action</b-dropdown-item>
			    <b-dropdown-item disabled>Disabled action</b-dropdown-item>
			  </b-dropdown> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			  <b-button variant="outline-primary" @click="addcards(index)">Add Card</b-button>
			  <b-button variant="outline-primary" @click="cards_download(index)">Export</b-button>
		</div>  
              <h2>{{lists[index]}}</h2>
              <p>This is {{lists[index]}} list</p>
        </div>





		<div v-for="cardsInfo in cards_data">
		 <div v-if="Object.keys(cardsInfo).length != 0">
		 <div v-for="y in Object.entries(cardsInfo)">
		  <div v-if="y[1][6] == index">
		  
		  <b-card :title="y[1][0]"  bg-variant="dark" text-variant="white">

        <div>
			  <b-dropdown id="dropdown-1" text= "Action" variant="outline-danger" class="m-md-2">
			    <b-dropdown-item @click="y[1][2] || y[1][7] == 'Deadline passed' ? stop_update() : updatecard(index, y[0], y[1][0], y[1][1])">Update card</b-dropdown-item>
			    <b-dropdown-item @click="deletecard(index, y[0])">Delete card</b-dropdown-item>
			    <b-dropdown-divider></b-dropdown-divider>
			    <b-dropdown-item active>Active action</b-dropdown-item>
			    <b-dropdown-item disabled>Disabled action</b-dropdown-item>
			  </b-dropdown> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              
			  <b-dropdown id="dropdown-1" text= "Move to" variant="outline-success" class="m-md-2">
			    <b-dropdown-item v-for="(l, ind) in lists" v-if="ind != index" @click="move_card(ind, y[1][0], y[1][1], y[1][5]); deletecard(index, y[0]);">{{ lists[ind] }}</b-dropdown-item>
			    <b-dropdown-divider></b-dropdown-divider>
			    <b-dropdown-item active>Active action</b-dropdown-item>
			    <b-dropdown-item disabled>Disabled action</b-dropdown-item>
			  </b-dropdown> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;


		</div> <br>

		    <b-card-text>
		      <h6>{{ y[1][1] }}</h6>
		    </b-card-text> <br> <br>
	       <h4>Status: {{ y[1][7] }}</h4>
		   <em> Deadline: {{ y[1][5] }} </em><br>
		   <em> Completed at: {{ y[1][4] }} </em><br>
		    <em> created at: {{ y[1][3] }} </em>
		    


		  </b-card>
		  </div>
		  </div>
		 </div> 
		  
		</div>





          
        </article>
      </section>
      <button type="button" class="btn btn-primary" @click="addlists">Add lists</button>
    </div>
  </main>
</div>





	`,
	data() {
		return{
		
		lists: null,
		cards_data: [],

		}
	},
	methods: {
		deletelists(id) {
        CustomFetch(`http://localhost:5000/api/${id}/delete/`, {
	        method: 'DELETE',
	        headers: {
	          'Authentication-Token': localStorage.getItem('Authentication-Token'),
	        }
	      })
	        .then(() => {
	          delete this.lists[id];
              localStorage.removeItem('card-data')
              this.$router.push({ path: '/lists' })	          
	        })
	        .catch((err) => {
	          alert(err.message)
	        })
    },
        addlists() {
              this.$router.push({path: '/add_list_form'})
        },
        edittitle(id) {
        	  this.$router.push({name: 'new_list_title', params: {value: id}})
        },
        addcards(id) {
			  this.$router.push({name: 'new_card', params: {value: id}})
        },


        updatecard(id, cards_id, title, content) {

              this.$router.push({name: 'update_card', params: {value: [id, cards_id, title, content]}})  	

        },

        deletecard(id, cards_id) {
        CustomFetch(`http://localhost:5000/delete_card/${id}/${cards_id}/`, {
	        method: 'DELETE',
	        headers: {
	          'Authentication-Token': localStorage.getItem('Authentication-Token'),
	        }
	      })
	        .then(() => {
				this.$router.push({path: '/lists'})


	        })
	        .catch((err) => {
	          alert(err.message)
	        })        	

        },
        stop_update(){
        	alert("Can not update")
        },

        move_card(ind, title, content, deadline){
        	var form_info = {
            	card_title: title,
            	content: content,
            	deadline: deadline
            }
			CustomFetch(`http://localhost:5000/add_card/${ind}/`, {
				method: 'POST',
				body: JSON.stringify(form_info),
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("card moved successfully")
				this.$router.push({path: '/lists'})
			})
			.catch((err) =>{
				alert(err.message)
			})
        },

        logout(){
          localStorage.removeItem('Authentication-Token')
          localStorage.removeItem('list-data')
          localStorage.removeItem('card-data')
          this.$router.push({ path: '/' })
        },

        summary_view(){
        	this.$router.push({name: 'summary_comp', params: {value1: this.cards_data}})
        },

        list_download(){
			CustomFetch(`http://localhost:5000/list/download/`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("Please check your email, your list data has been sent.")
			})
			.catch((err) =>{
				alert(err.message)
			})
        },

        cards_download(index){
			CustomFetch(`http://localhost:5000/cards/${index}/download/`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': '*', 
					'Authentication-Token': localStorage.getItem('Authentication-Token'),
				}

			})
			.then((data) => {
				alert("Please check your email, your list data has been sent, if you have any.")
			})
			.catch((err) =>{
				alert(err.message)
			})
        } 

        



},

	
	created() {
		    let new_list = [];
			CustomFetch(`http://localhost:5000/api/get_lists/`, {
				method: 'GET',
				headers: {
                   
                   'Authentication-Token': localStorage.getItem('Authentication-Token'),
                   'Content-Type': 'application/json',
                   'Access-Control-Allow-Origin': '*',

                }
			})
			.then((data) => {
				new_list.push(data)
				this.lists = new_list[0];
				localStorage.setItem('list-data', JSON.stringify(new_list[0]))
				console.log(new_list[0]) 



				for(var x of Object.keys(new_list[0])){
				CustomFetch(`http://localhost:5000/api/get_cards/${x}/`, {
				method: 'GET',
				headers: {
                   
                   'Authentication-Token': localStorage.getItem('Authentication-Token'),
                   'Content-Type': 'application/json',
                   'Access-Control-Allow-Origin': '*',

	                }
				})
				.then((data) => {
					this.cards_data.push(data)
					localStorage.setItem('card-data', JSON.stringify(this.cards_data)) 

				})
				.catch((err) =>{
					console.log(err.message)
				})

		        
			}




                


				

			})
			.catch((err) =>{
				console.log(err.message)
			})

			
               
		},
	
}
