<script>
import { Line, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["chartdata", "options"],
  mounted() {
    if (!this.options) {
      this.options = {
        responsive: true,
        // title: {
        //   display: true,
        //   text: "Chart.js Line Chart",
        // },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          x: {
            display: true,
            scaleLabel: {
              display: true,
              labelString: "Mês",
            },
          },
          y: {
            display: true,
            scaleLabel: {
              display: true,
              labelString: "Value",
            },
          },
        },
      };
    }
    this.renderChart(this.chartdata, this.options);
  },
};
</script>