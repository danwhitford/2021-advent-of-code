(ns day12
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "start-A
start-b
A-c
A-b
b-d
A-end
b-end"))


(defn split-line
  {:test #(t/is (= ["start" "A"] (split-line "start-A")))}
  [line]
  (str/split line #"-"))

(defn get-graph
  [lines]
  (let [sp (map split-line lines)]
    (reduce (fn [g p] {:nodes (distinct (concat (:nodes g) p)) :edges (conj (:edges g) {:from (first p) :to (second p)} {:from (second p) :to (first p)})}) {:nodes [] :edges []} sp)))

(defn small-cave?
  [n]
  (cond
    (= n "start") false
    (= n "end") false
    :else (every? #(Character/isLowerCase %1) n)))

(defn almost-flatten
  [x]
  (filter #(and (sequential? %) (not-any? sequential? %))
          (rest (tree-seq #(and (sequential? %) (some sequential? %)) seq x))))

(defn contains-dupe?
  [col]
  (loop [[hd & rst] col found #{}]
    (cond
      (nil? hd) false
      (contains? found hd) true
      :else (recur rst (conj found hd)))))

(defn get-routes
  [g n p]
  (if (= n "end")
    p
    (let [nxts (->> (:edges g)
                    (filter #(= (:from %1) n)) ;; From this node
                    (map :to)
                    (remove #(= "start" %1)) ;; Don't go back to start
                    (remove #(and 
                              (small-cave? %1) 
                              (some (fn [pp] (= %1 pp)) p)
                              (contains-dupe? (filter small-cave? p)))))] ;; Small cave that has been visited AND another has been visited twice
      (almost-flatten (map #(get-routes g %1 (conj p %1)) nxts)))))

(defn solve
  {:test #(t/is (= 36 (solve example-in)))}
  [lines]
  (let [g (get-graph lines)]
    (->> (get-routes g "start" ["start"])
         (filter vector?)
         count)))

(t/run-tests)
