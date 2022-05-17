function (doc) {
  emit([doc.location, doc.district, doc.time.time_of_day.substr(0, 2)],1)
}
