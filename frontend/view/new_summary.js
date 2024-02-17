import CustomFetch from '../CustomFetch.js'
import summary_page from './summary_page.js'
export default {
	template: `
	   <div>
       <h1 style="color:green;">Summary</h1> <router-link to="/lists"><h5>Go to Home</h5></router-link> <br><br>	   

       <div>
       <h5><em>Total number of tasks pending across the lists: {{ due }}</em> <br></h5>
       <h5><em>Total number of tasks across the lists: {{ total }}</em> <br></h5>
       <h5><em>Total number of tasks completed across the lists: {{ complete }}</em> <br></h5>
       <h5><em>Total number of tasks for which due date is passed: {{ over }}</em></h5>

         <bar-chart :width="80" :height="25" />
       </div>
       </div>

	`,
	data(){
		return{
			new_value: this.$route.params.value1,
			val: JSON.parse(localStorage.getItem('card-data')),
			new_list: [],
			total: 0,
			complete: 0,
			over: 0,
			due: 0
		}
	}, 

	mounted() {
		for(var x of this.val){
			for(var y in x){
				this.total += 1
		        if(x[y][7] == 'Completed'){
                   this.complete += 1
		        }
		        else if(x[y][7] == 'Deadline passed'){
		            this.over += 1
		        }
		        else if(x[y][7] == 'Task is due'){
		            this.due += 1
		        }		        
		    }
		}
	}

}