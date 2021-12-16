(ns day2)
(require
 '[clojure.string]
 '[clojure.test]
 '[clojure.spec :as s])

(def example-in (clojure.string/split-lines "forward 5
down 5
forward 8
up 3
down 8
forward 2"))

(defmacro is-eq [expected actual]
  (list 'clojure.test/is (list '= expected actual)))

(s/def :day2/dir #{"forward" "up" "down"})
(s/def :day2/val int?)
(s/def :day2/order (s/keys :req-un [:day2/dir :day2/val]))

(defn get-orders
  {:test #(is-eq
           '({:dir "fd" :val 1} {:dir "lt" :val 90})
           (get-orders '("fd 1" "lt 90")))}
  [s]
  (->> s
       (map #(clojure.string/split %1 #"\s+"))
       (map #(hash-map :dir (first %1) :val (Integer/parseInt (nth %1 1))))))

(defn move
  {:test #(clojure.test/is
           (=
            {:pos 0 :depth 0 :aim 10}
            (move {:pos 0 :depth 0 :aim 0} {:dir "down" :val 10})))}
  [status order]
  (let [{dir :dir val :val} order]
    (cond
      (= dir "forward")
      (-> status
          (update ,,, :pos #(+ %1 val))
          (update ,,, :depth #(+ %1 (* (:aim status) val))))
      (= dir "up") (update status :aim #(- %1 val))
      (= dir "down") (update status :aim #(+ %1 val)))))

(defn follow-orders
  [orders]
  {:pre [(s/valid? (s/coll-of :day2/order) orders)]}
  (reduce move {:depth 0 :aim 0 :pos 0} orders))

(defn mul-pos
  {:test #(clojure.test/is (= 500 (mul-pos {:pos 50 :depth 10 :aim 90})))}
  [s]
  (* (:pos s) (:depth s)))

(defn solve
  "Solve day 2 given an input seq"
  {:test #(clojure.test/is (= 900 (solve example-in)))}
  [s]
  (-> s get-orders follow-orders mul-pos))

