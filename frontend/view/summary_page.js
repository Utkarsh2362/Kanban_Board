export default Vue.component("bar-chart", {
  extends: VueChartJs.Bar,


  data(){
  	return{
       val: []
  	}
  },

  mounted() {
  	var lists = JSON.parse(localStorage.getItem('list-data'))
  	var cards = JSON.parse(localStorage.getItem('card-data'))
  	var count = {};
    for(var p in lists){
       count[p] = 0
    }

    for(var x in lists){
       for(var y of cards){
           for(var a of Object.values(y)){
            //console.log(a)
             if(a[2] == true){
                count[a[6]] += 1
            }
        }
    }break;
}

  	for(var x in lists){
        this.val.push(lists[x]);   
  	}
    this.renderChart(
        {
            labels: this.val,
            datasets: [{
                label: "Completed Task",
                data: Object.values(count),
                fill: false,
                barThickness: 100,
                backgroundColor: "#eebcde ",
                borderColor: "#eebcde",
                borderCapStyle: 'butt',
                borderDash: [5, 5],
            }],

            options: {
            maintainAspectRatio: false,	
            responsive: true,
            scales: {
            y: {
                beginAtZero: true,
                }
            }
        }        
    }

    

       
    



    );
  },
});


