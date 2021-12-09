(ns day3)

(require
 '[clojure.string :as str]
 '[clojure.test :as t])

(def example-input (str/split-lines "00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"))

(defn zipup
  [lines]
  (apply map vector lines))

(defn nth-uncommonest
  [n tie]
  (fn [s] (let [f (frequencies s)
        sorted-f (sort-by val f)]
    (if (= (first (vals sorted-f)) (second (vals sorted-f)))
      tie
      (nth (keys sorted-f) n)))))

(defn bin-to-num
  [bin-str]
  (Integer/parseInt bin-str 2))

(defn filter-candidates
  [bit-criteria]
  (fn [candidates i] (-> candidates
    (zipup)
    (nth ,,, i)
    (bit-criteria)
    (as-> $$ (filter #(= (nth %1 i) $$) candidates)))))
 
(defn get-life-support-status
  [filter-fn]
  (fn [candidates]
    (loop [candidates candidates i 0]
      (if (= (count candidates) 1)
        (first candidates)
        (recur
         (filter-fn candidates i)
         (inc i))))))

(def oxygen-filter (filter-candidates (nth-uncommonest 1 \1)))
(def co2-filter (filter-candidates (nth-uncommonest 0 \0)))

(def get-oxygen (get-life-support-status oxygen-filter))
(def get-co2 (get-life-support-status co2-filter))

(defn solve
  {:test #(t/is (= 230 (solve example-input)))}
  [lines]
  (let
   [oxygen (get-oxygen lines)
    co2 (get-co2 lines)]
    (* (bin-to-num oxygen) (bin-to-num co2))))

(t/run-tests)
