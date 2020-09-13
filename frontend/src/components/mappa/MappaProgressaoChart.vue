<script>
import { Line, mixins } from "vue-chartjs";

export default {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ["options"],
  computed: {
    cmpOptions() {
      if (!this.options) {
        return {
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
      return this.options;
    },
  },
  mounted() {
    this.renderChart(this.chartdata, this.cmPoptions);
  },
};
</script>