(ns day1)

(require 'clojure.java.io)

(defn f-seq [fname]
  (let [rdr (clojure.java.io/reader fname)]
    (line-seq rdr)))

(->> (f-seq "res/day1_in")
     (map #(Integer/parseInt %1))
     (partition 3 1)
     (map #(apply + %1))
     (partition 2 1)
     (map #(apply compare %1))
     (filter neg?)
     (count))

