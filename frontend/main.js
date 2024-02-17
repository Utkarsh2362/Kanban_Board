import login from '././view/login.js'
import signup from '././view/signup.js'
import list from '././view/list.js'
import form from '././view/form.js'
import list_update from '././view/list_update.js'
import card from '././view/card.js'
import card_update from '././view/card_update.js'
import summary_page from '././view/summary_page.js'
import new_summary from '././view/new_summary.js'


const routes = [
  { path: '/signup', component: signup },
  { path: '/', component: login }, 
  { path: '/lists', component: list },
  { path: '/add_list_form', component: form },
  { path: '/update_list_form', name: 'new_list_title',  component: list_update, params: true }, 
  { path: '/create_card', name: 'new_card',  component: card, params: true },
  { path: '/update_card_form', name: 'update_card',  component: card_update, params: true },
  { path: '/summary', component: summary_page },
  { path: '/new_summary',name: 'summary_comp', component: new_summary, params: true }, 
]


const router = new VueRouter({
  routes
})

var app = new Vue({
	el: "#app",
	template: `
			<div class="container">
			  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
			  <a class="navbar-brand">Kanban</a>
			    <div class="collapse navbar-collapse" id="navbarNav">
			    <ul class="navbar-nav">
			      <li class="nav-item"><router-link class="nav-link" to="/">Login</router-link> </li>
			      <li class="nav-item"><router-link class="nav-link" to="/signup">Signup</router-link> </li>
			    </ul>
			  </div>
			 </nav>

			    <div class="row">
			        <div class="col">
			       <router-view></router-view>
			        </div>    
			    </div>
			</div>



	`,
	data: {
		name: "Utkarsh Kumar Yadav"
	},
	router,

	components: {
		'login': login,
		'signup': signup,
		'list': list,
		'form': form,
		'list_update': list_update,
		'card': card,
		'card_update': card_update,
		'summary_page': summary_page,
		'new_summary' : new_summary
	}
})