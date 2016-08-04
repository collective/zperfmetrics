{
    port: 8125,
	  debug: false,
    deleteGauges: true,
    flushInterval: 5000,
    backends: [ "./backends/graphite"],
    graphite: {
        legacyNamespace: false
    },
    graphitePort: 2003,
    graphiteHost: "graphite"
}
