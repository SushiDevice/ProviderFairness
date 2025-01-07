MOReGIn: Multi-Objective Recommendation
at the Global and Individual Levels

Elizabeth G´omez1[0000−0003−2698−3984], David Contreras2[0000−0002−6906−485X],
Ludovico Boratto3[0000−0002−6053−3015], and Maria Salam´o1[0000−0003−1939−8963]

1 Facultat de Matem`atiques i Inform`atica, Universitat de Barcelona, Barcelona, Spain
egomezye13@alumnes.ub.edu,maria.salamo@ub.edu
2 Facultad de Ingenier´ıa y arquitectura, Universidad Arturo Prat, Iquique, Chile
david.contreras@unap.cl
3 Department of Mathematics and Computer Science, University of Cagliari,
Cagliari, Italy ludovico.boratto@acm.org

Abstract. Multi-Objective Recommender Systems (MORSs) emerged
as a paradigm to guarantee multiple (often conflicting) goals. Besides ac-
curacy, a MORS can operate at the global level, where additional beyond-
accuracy goals are met for the system as a whole, or at the individual
level, meaning that the recommendations are tailored to the needs of each
user. The state-of-the-art MORSs either operate at the global or individ-
ual level, without assuming the co-existence of the two perspectives. In
this study, we show that when global and individual objectives co-exist,
MORSs are not able to meet both types of goals. To overcome this issue,
we present an approach that regulates the recommendation lists so as
to guarantee both global and individual perspectives, while preserving
its effectiveness. Specifically, as individual perspective, we tackle genre
calibration and, as global perspective, provider fairness. We validate our
approach on two real-world datasets, publicly released with this paper4.

Keywords: Multi-Objective Recommendation · Calibration · Provider Fairness.

1

Introduction

Motivation. Since the goal of recommender systems is to provide relevant sug-
gestions for the users, the main focus has been the effectiveness of the results [37].
Nevertheless, users might be interested in properties of the items besides their
effectiveness, and there are other stakeholders who can benefit from how rec-
ommendations are produced (e.g., content providers). Hence, beyond-accuracy
perspectives are central to the generation and evaluation of recommendations.
Multi-Objective Recommender Systems (MORSs) support the provision of
perspectives that go beyond item relevance, such as, e.g., diversity, calibration,
and fairness [49]. The optimization for these objectives can happen at the global
(aggregate) level, thus ensuring that the system as a whole can guarantee certain
properties (e.g., all providers receive a certain exposure in the recommendation
lists). In alternative, a MORS can operate at the individual (local) level, and

2

G´omez et al.

shape results that are consider the prominence of individual users towards the
different goals (e.g., each user can receive a different level of diversity or the
recommended genres can be calibrated to the preferences in the training set) [21].
When analyzing the current literature, a MORS either operates at the global

level [15,26,28,32,44] or at the local level [34,8,7].

Open issues. There might be scenarios in which both global and individual
objectives co-exist. Indeed, a platform might decide that, as a whole, the recom-
mendations should offer certain properties (e.g., be fair to providers of different
demographic groups, or enable a certain level of novelty). Moreover, specific
goals might be set for the individual users (e.g., the calibration of the genres or
the diversity of the recommended items might need to follow what is observed
in the training set of each user). As we show in Section 6, when a MORS tackles
only global or individual perspectives, the other perspective trivially remains
under-considered and cannot be guaranteed by the system.

Our contributions. To overcome the aforementioned challenges, in this paper,
we present a MORS that produces recommendations with both global and in-
dividual objectives. As a use case, we consider, as a global objective, provider
fairness and, as an individual one, calibrated recommendations. This aligns our
study with the rest of the MORS literature, where two beyond-accuracy objec-
tives are considered. For the sake of clarity, we will talk about provider-fair and
calibrated recommendations but, as we discuss in Section 3.2, our approach
can be generalized to any global or individual objective.

Besides accounting for beyond-accuracy perspectives involving both global
and individual objectives, the problem of providing provider-fair and calibrated
recommendations becomes interesting also from a practical point of view. As we
will show in Section 4, users tend to rate items of certain genres and that are
produced in certain geographic areas, suggesting that we can account for both
perspectives at the same time when generating the recommendations. Hence, at
the technical level, we would need a unique solution that (i) produces effective
results for the users, (ii) can provide fairness for providers belonging to different
groups at the global level, i.e., by distributing, over the entire user base, the
recommendation of items belonging to different provider groups in equitable
ways, and (iii) can calibrate the recommendation lists of each individual user.

Our approach involves a post-processing strategy. To enable a form of provider
fairness that can consider demographic groups that are not necessarily charac-
terized by a binary group (e.g., males and females), we consider, as a sensitive
attribute, the geographic provenance of the providers and have the different con-
tinents as the granularity with which we split the groups; this is aligned with
recent literature on provider fairness [17,18]. As in classic calibrated fashion,
we distribute the recommendations according to the item genre. Based on this
characterization of the data, we present an approach that makes use of buckets
to associate the continents in which the items are produced and the genre of the
items. We use these buckets to post-process the recommendation lists (we will
later discuss that this is the best way to regulate both aggregate- and individual-
level properties) and regulate how the recommendations are distributed across

MOReGIn: Multi-Objective Recommendation

3

the users. Thanks to the fact that each bucket contains (i) the continent in which
the item is produced, to regulate provider fairness, and (ii) the genre of the item,
to regulate calibration, both global and individual perspectives are captured at
once by our approach. To validate our proposal, we apply it to the recommenda-
tions produced by five algorithms, and study the effectiveness of our approach
on two datasets (including a novel one, released with this study), and against
state-of-the-art approaches for calibrated recommendation and provider fairness.

Concretely, our contributions can be summarized as follows:

– After the identification of the research gaps (Section 2) and characterization
of our setting (Section 3), we provide the foundations to our use case, by
showing that calibration and provider fairness are related problems, since the
genres of the items and their country of production are connected (Section 4);
– We present an approach to post-process the recommendation lists to meet
both global and individual goals. We calibrate the results for the individual
users in terms of genres, and are fair towards providers (Section 5);

– We face the limitation of evaluating this problem, due to the scarcity of
data offering both the category of the items and the sensitive attributes
of the providers, so we i) extend the MoviLens-1M dataset, to integrate
the continent of production of each item, and ii) we collect and present (in
Section 3) a novel dataset. Both resources are publicly available here4;
– We perform experiments (Section 6) to validate our proposal when applied
to the recommendation produced by five algorithms, covering both memory-
and model-based approaches, and point-wise and pair-wise approaches. To
evaluate its effectiveness in different domains, we consider movie and song
recommendation as application scenarios. Based on our outcomes, we high-
light possible research paths that might emerge from it (Section 7).

2 Related Work

MORSs. Recent literature has studied how to account for multi-objective goals
from different angles. The user perspective was tackled by Li et al [26], which bal-
ance recommendation accuracy for users with different levels of activities. From
an item perspective, Ge et al. [15] proposed an approach to balance item rele-
vance and exposure. Considering both the user and item perspectives, Naghiaei
et al. [32] propose a re-ranking approach to account for consumer and provider
fairness. Other studies blend the multiple objectives into a single function, in
order to obtain a Pareto-optimal solution [28,44]. Recent advances have also
proposed MORSs in sequential settings, by optimizing the results for accuracy,
diversity, and novelty [41]. MORS that operate at the individual level have opti-
mized the recommendation process mainly via online interactions, such as con-
versational approaches [25] or via critiquing [43,12], but approaches aiming at
learning individual propensities from past interactions also exist, e.g., [22,34,8,7].

4 https://tinyurl.com/yc6nnx5v

4

G´omez et al.

Calibrated recommendation. Calibration is a well-studied technique com-
monly used to solve the problem of unfair output [33,46,42] in recommender
systems. Seymen et al. [40] address the problem of providing calibration in the
recommendations from a constrained optimization perspective. Abdollahpouri et
al. [1] study the connection between popularity bias, calibration, and consumer
fairness in recommendation. Recently, Rojas et al. [38] analyze how the cali-
bration method in [42] deals with the bias in different recommendation models.
Other studies focus on analyzing user profiles to mitigate miscalibrated recom-
mendations [27] or to mitigate popularity bias from the user’s perspective [6].
Existing metrics have some limitations when applying a user-centered approach
to evaluate popularity bias and calibrated recommendations. To address these
limitations, Abdollahpouri et al. [2] present a new metric.

Provider fairness. Provider fairness [9] has been studied in many common
scenarios, e.g., [29,18,11,10,16,14,30]. It is usually assessed by considering metrics
such as the visibility and the exposure that respectively assess the amount of
times an item is present in the rankings [13,47] and where an item is ranked [5,48],
for users to whom each provider’s items are recommended. Other approaches,
such as that by Karakolis et al. [23], consider diversity and coverage for users.
Raj et al. [35] present a comparative analysis among several fairness metrics
recently introduced to measure fair ranking. Wu et al. [45] formalize a family
of exposure fairness metrics that model the problem of fairness jointly from the
perspective of both types of stakeholders.

Contextualizing our work. No MORS can address both calibrated recom-
mendation lists for the users and provider fairness. Our algorithm’s aims are to
provide i) each user with calibrated recommendations, ii) fair recommendations
for the providers, iii) aiming at a minimum loss in effectiveness.

3 Preliminaries

3.1 Recommendation Scenario

Let U = {u1, u2, ..., un} be a set of users, I = {i1, i2, ..., ij} be a set of items,
and V be a totally ordered set of values that can be used to express a preference
together with a special symbol ⊥. The set of ratings results from a map r :
U × I → V , where V is the rating domain. If r(u, i) = ⊥, then we say that u
did not rate i. To easy notation, we denote r(u, i) by rui. We define the set of
ratings as R = {(u, i, rui) : u ∈ U, i ∈ I, rui ̸= ⊥} and they can directly feed
an algorithm in the form of triplets (point-wise approaches) or shape user-item
observations (pair-wise approaches). We denote with Ru the ratings associated
with a user u ∈ U . We consider a temporal split of the data, where a fixed
percentage of the ratings of the users (ordered by timestamp) goes to the training
and the rest goes to the test set [4]. The goal is to learn a function f that
estimates the relevance (ˆrui) of the user-item pairs that do not appear in the
training data (i.e., rui = ⊥). We denote as ˆR the set of recommendations.

MOReGIn: Multi-Objective Recommendation

5

Let C denote the set of geographic continents in which items are organized.
We consider a geographic continent as the provenance of an item provider. We
denote as Ci the set of geographic continents associated with an item i. Note
that, since an item could be produced by more than one provider, it might be
associated with several geographic continents, and thus, |Ci| ≥ 1 and Ci ⊆ C.
In case two providers belong to the same geographic continent, that continent
appears only once; indeed, we are dealing with group fairness so, when a group
of providers is associated with an item (once or multiple times), we account for
its presence. We use the geographic continents to shape demographic groups,
which can be defined to group the ratings of the items produced in a continent
(we denote the items in I produced in a continent c ∈ C as Ic, where Ic ⊆ I ).
Let G denote the set of genres in which items are organized. We denote as
Gi the set of genres associated with an item i. Note that, an item can be of one
or more genres, and thus, |Gi| ≥ 1 and Gi ⊆ G . We denote the items in I that
have a genre g ∈ G as Ig, where Ig ⊆ I.

3.2 Metrics

Provider-group Representation. In order to enable provider fairness, we
should understand the attention received by a provider group in the training
data. For this reason, we compute the representation of a demographic group in
the data as the number of ratings for items associated with that group in the
data. We define with R the representation of a group c ∈ C as follows:

Rc =

|{rui : u ∈ U, i ∈ Ic}|
|R|

(1)

Eq. (1) accounts for the proportion of ratings given to the items of a demo-
graphic group associated with a continent. This metric ranges between 0 and
1. We compute the representation of a group only considering the training set.
Trivially, the sum of the representations of all groups is equal to 1.

User-based genre propensity. In order to calibrate the results for the users,
we need to understand how the preferences for the different item genres are
distributed. For this reason, we define with P the propensity of a user of u ∈ U
to rate items of a genre g ∈ G, as follows:

Pug =

|{rui : g ∈ Gi}|
|Ru|

(2)

Eq. (2) accounts for the proportion of ratings associated with a genre for
a given user. This metric ranges between 0 and 1. Trivially, the sum of the
propensities of all genres for a user is equal to 1. This metric is equivalent to the
distribution p(g|u) [42].

Disparate Impact. We assess unfairness with the notion of disparate impact
generated by a recommender system. Specifically, we assess disparate visibility.

6

G´omez et al.

Definition 1 (Disparate visibility). Given a group c ∈ C, the disparate vis-
ibility returned by a recommender system for that group is measured as the dif-
ference between the share of recommendations for items of that group and the
representation of that group in the input data:

(cid:32)

∆Vc =

1
|U |

(cid:88)

u∈U

|{ˆrui : i ∈ Ic}|
| ˆR|

(cid:33)

− Rc

(3)

The range of values for this score is [−Rc, 1 − Rc]; specifically, it is 0 when the
recommender system has no disparate visibility, while negative/positive values
indicate that the group received a share of recommendations that is lower/higher
than its representation. This metric is based on that defined by Fabbri et al. [13].
Miscalibration. We assess the tendency of a system to recommend a user items
whose genres are distributed differently from those they prefer via miscalibration.

Definition 2 (Miscalibration). Given a user u ∈ U and a genre g ∈ G, the
miscalibration returned by a recommender system for that user is measured as
the difference between the share of recommendations for items of that genre and
the propensity of the user for that genre in the training data:

∆Mug =

|{ˆrui : i ∈ Ig}|
| ˆRu|

− Pug

(4)

Generalizability. The rest of our paper will consider disparate visibility (∆Vc)
as the global perspective and miscalibration (∆Mug) as the individual perspec-
tive our MORS considers. Nevertheless, our approach can be generalized to any
metric that assesses the difference between (i) the distribution of the recommen-
dations and (ii) what can be observed in the training set or an objective set by
the platform via a policy (e.g., a given amount of content novelty or diversity).

4 Matching Item Providers and Genre Propensity

4.1 Real-world Datasets

First, we extended the MovieLens-1M dataset, so as to integrate the continent
of production of each movie. Second, a domain that fits our problem is song
recommendation. However, existing music datasets, such as LastFM-2B [31], do
not contain song genres and sensitive attributes of the artists, so they do not fit
our problem. Thus, we collected a dataset from an online music platform.

In particular, the MovieLens-1M (Movies) dataset comprises 1M ratings
(range 1-5), from 6,040 users for 3,600 movies across 18 genres. The dataset pro-
vides its IMDB ID, which allowed us to associate it to its continent of production,
thanks to the OMDB APIs (http://www.omdbapi.com/). Keep in mind that a
movie may be produced on more than one continent. On the other hand, Be-
yondSongs (Songs) contains 1,777,981 ratings (range 1-5), provided by 30,759
users, to 16,380 songs. For each song, we collected the continent of provenance
of the artist, and 14 music genres. Both resources are available online4.

MOReGIn: Multi-Objective Recommendation

7

(a) Movies Rc

(b) Songs Rc

(c) Movies Pug

(d) Songs Pug

Fig. 1: Group representation (a and b) and genre propensity (c and d) in the
Movies and Songs data. Acronyms stand for AF: Africa, AS: Asia, EU: Europe,
NA: North America, OC: Oceania, SA: South America.

4.2 Characterizing Group Representation and Genre Propensity

We consider the temporal split of the data, where 80% of the ratings are con-
sidered for the training set and have been used to measure Rc and Pug. Note
that, while the representation of a demographic group covers the entire training
set, the propensity is measured at the user level. Hence, to characterize the link
between the two phenomena we aggregate the propensity of all the users for a
given genre by summing their values.

Figures 1a and 1b show the Rc for Movies and Songs, respectively. Both
datasets depict a similar representation by continents, where the highest repre-
sentation is of items from NA providers (72% in movies and 64% in songs) and
the second place is for EU providers (23% and 29%). In the rest of the conti-
nents, for both datasets, it is less than 10%. Figures 1c and 1d show the Pug in
both datasets; three genres attract most of the ratings by users.

We can also observe that ratings seem to be clustered between certain genre-
continent pairs. In other words, different genres are distributed differently across
continents. In the Movies data (Fig. 1c), Comedy movies are largely preferred
when produced by EU producers, just as Action attracted the majority of ratings
for movies by NA producers. In the Songs data (Fig. 1d), the Electronic/Dance
genre was consumed much more heavily when produced by EU artists than by

0%3%23%72%2%0%0,0000,1000,2000,3000,4000,5000,6000,7000,800AFASEUNAOCSA0%3%29%64%2%1%0,0000,1000,2000,3000,4000,5000,6000,7000,800AFASEUNAOCSA0,0000,1000,2000,3000,4000,500FantasyWarRomanceWesternDocumentaryMusicalFilm-NoirSci-FiMysteryThrillerChildren'sCrimeAnimationHorrorAdventureDramaActionComedyAFASEUNAOCSA0,0000,1000,2000,3000,4000,500GospelClassicSoundtrackAlternativeFolkBluesJazzSoul/FunkCountryHeavy metalElectronic/DanceRap/Hip-hopPopRockAFASEUNAOCSA8

G´omez et al.

those in the rest of the world, and Heavy metal songs are mostly consumed
when they come from NA. In both datasets, users’ preferences for the minority
provider groups (AF, AS, OC, and SA) are also concentrated on a few selected
genres, confirming this rating aggregation in certain genre-continent pairs.

Observation 1. Users have the propensity to rate items of certain genres
and that are produced by certain geographic groups (i.e., in certain conti-
nents). Calibration and provider fairness are related problems so, when pro-
ducing recommendation lists, both perspectives should be accounted at the
same time, in MORS fashion.

5

Individually Calibrated and P-Fair Recommendation

5.1 Algorithm

MOReGIn adjusts the recommendations according to the continent of the
providers and the representation of each demographic group and seeks to make
a calibration at the individual level, following the propensity of each user to
rate items of a given genre. Formally, MOReGIn (see Algorithm 1) works fol-
lowing four main steps. Steps 1 and 2 are devoted to compute Rc and Pug,
considering the ratings in the training set. Step 3 computes the items that were
predicted as relevant for a user by the recommender system and creates a bucket
list, joinBucket, considering each continent-genre pair, which will store the pre-
dicted items. Each bucket comes with two attributes: Rc and Pug. Specifically,
the recommender system returns a list of top-n recommendations (where n is
much larger than the cut-off value k, so as to be able to perform a re-ranking).
Our starting point to fill a bucket is the relevance predicted for a user u and an
item i, ˆrui. That item will be stored in the buckets associated with each genre
g ∈ Gi and each continent c ∈ Ci (even though an item may appear in more
than one bucket, it can only be recommended only once). Each element in the
bucket is a record that contains the item ID and the ˆrui. We sort each bucket
considering three values. We sort out Rc and Pug, in ascending order to ensure
the inclusion in the recommendation lists of items from genres and continents
that are less represented in the dataset, and we sort in descending order by
rating to enhance those products that are relevant to the user. Finally, Step 4
performs a three-phase re-ranking based on the generated bucket lists. Phase 1
is where we begin, and subsequent phases occur until the top-k is complete. In
detail, Phase 1 selects items starting from the least represented continents to
the most represented ones in their corresponding buckets. The algorithm selects
items with these conditions: (1) the percentage of items in the recommendation
list for a continent is lower or equal to the representation of the continent (Rc);
(2) the percentage of items of a given genre in the top-k is lower or equal than
Pug · k; and (3) the number of recommended items so far is lower than k. Phase
2 relaxes the restrictions of phase 1 and here condition 2 is not applied. Phase 3
selects the items that have the greater relevance for the user, until we complete
the top-k. That is, conditions 1 and 2 are not considered.

MOReGIn: Multi-Objective Recommendation

9

Input: recList: ranked list (records contain user, item, rating, position,

genre , continent), which arrives sorted by user and rating and
contains topn recommendations to the user.
trainList: list with the training set (records contain user, item,
rating, genre, continent), which is sorted by user and rating.
topk: top k recommendations, we set up k = 10.
topn: top n recommendations, we set up n= 1000.

Output: reRankedList: ranked list with Individually Calibrated and P-Fair

Recommendation.

1 define MOReGIn (recList, trainList, topk, topn)
2 begin

3

4

5

6

7

8

9

// Step 1. Compute Rc
recBucketRep ← computeRepresentation(topk, recList, trainList);
// Step 2. Compute Pug
recBucketU serP rop ← computePropensity(topk, recList, trainList);
// Step 3. Create a bucket list
joinBucket ← recList + recBucketRep + recBucketU serP rop;
joinBucket ← sort(joinBucket);
// Step 4. Perform selection of items with three phases
userCounts, userGenCounts , contCounts ← ∅;
joinBucket ← selectWithHardConstraints(joinBucket,

recBucketRep, recBucketU serP rop, userCounts, userGenCounts,
contCounts) ; // Phase 1

joinBucket ← selectWithSoftConstraints(joinBucket, recBucketRep,

recBucketU serP rop, 2, userCounts, userGenCounts, contCounts) ;
// Phase 2

10

joinBucket ← selectWithSoftConstraints(joinBucket, recBucketRep,

recBucketU serP rop, 3, userCounts, userGenCounts, contCounts) ;
// Phase 3

reRankedList ← chooseSelectedItems(joinBucket);
reRankedList ← sort(reRankedList) ; // sort by user and rating
return reRankedList;

11

12

13
14 end

Algorithm 1: Pseudocode of MOReGIn algorithm

6 Experimental Evaluation

6.1 Experimental Methodology

In this work, we focus on well-known state-of-the-art Collaborative Filtering al-
gorithms: ItemKNN [39], UserKNN [20], BPRMF [36], SVDpp [24], and
NeuMF [19]). We will report the results of the original recommendation algo-
rithm (denoted as OR). We also consider two comparison baselines: (i) a greedy
calibration algorithm [42] (denoted as CL) with a λ value of 0.99 (setup defined
in [42]), which post-processes the recommendation lists generated by traditional
recommender systems; and (ii) a provider fairness algorithm [17] (denoted as
PF) that considers the providers’ continent provenance as a sensitive attribute,
with a re-ranking approach that regulates the share of recommendations given

10

G´omez et al.

1 define selectWithHardConstraints(joinBucket, recBucketRep,

recBucketU serP rop, userCounts, uGenCounts, contCounts) begin
expectedRecordsCont ← getExpectedRecordsCont(recBucketRep);
expectedRecU serGen ← getRecordsU serGen(recBucketU serP rop);
foreach rec ∈ joinBucket do // for each record

userGen ← rec.user + ” − ” + rec.genre;
if userGen ∈ expectedRecU serGen and
rec.cont ∈ expectedRecordsCont then

userCounts[rec.user] ← userCounts[rec.user] + 1;
uGenCounts[rec.userGen] ← uGenCounts[rec.userGen] + 1;
contCounts[rec.cont] ← contCounts[rec.cont] + 1;
if expectedRecUserGen[rec.userGen] ≥ userGenCounts and
expectedRecordsCont[rec.cont] ≥ contCounts and topk ≥
userCounts[rec.user] then

rec.phase ← 1; // selects element in phase 1
joinBucket.update(rec); // updates the element

end

end

end
return joinBucket

16
17 end
18 define selectWithSoftConstraints(joinBucket, recBucketRep,

recBucketU serP rop, phaseM OReGIn, userCounts, userGenCounts,
contCounts) begin

expectedRecordsCont ← getExpectedRecordsCont(recBucketRep);
foreach rec ∈ joinBucket do // for each record
if rec.cont ∈ expectedRecordsCont then

if phaseM OReGIn == 2 then

if expectedRecordsCont[rec.cont] ≥ contCounts and topk ≥

userCounts[rec.user] then

userCounts[rec.user] ← userCounts[rec.user] + 1;
contCounts[rec.cont] ← contCounts[rec.cont] + 1;
rec.phase ← 2; // selects element in phase 2
joinBucket.update(rec); // updates the element

end

end
if phaseM OReGIn == 3 then

if

topk ≥ userCounts[rec.user] then
contCounts[rec.cont] ← contCounts[rec.cont] + 1;
rec.phase ← 3; // selects element in phase 3
joinBucket.update(rec); // updates the element

end

end

end

2

3

4

5

6

7

8

9

10

11

12

13

14

15

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

end
return joinBucket

39
40 end

Algorithm 2: Selection methods for the MOReGIn algorithm

MOReGIn: Multi-Objective Recommendation

11

to the items produced in a continent (visibility) and the positions in which items
are ranked in the recommendation list (exposure).

To run the recommendation models, we used the Elliot framework [3], which
generated the recommendations for each user that fed the input of MOReGIn.
As noted in Section 4.2, the dataset was divided into two sets, one for training
(80%) and the other for testing with the most recent ratings of each user (20%).
For each user, we generated the top-1000 recommendations (denoted in the
paper as the top-n; we remind the reader that these n = 1000 results are
not shown to the users, they are only used internally by our algorithm) to
then re-rank the top-k (set up to 10) through the proposed MOReGIn al-
gorithm. We performed a grid search of the hyper-parameters for each model
in the two datasets. For ItemKNN and UserKNN, in both datasets, we use 50
neighbors, a cosine similarity, and the classical implementation. For BPRMF,
SVDpp, and NeuMf we defined 10 epochs and 10 factors on each dataset, ex-
cept NeuMF in Movies that uses 12 factors. The batch size is 512 for SVDpp
and NeuMF and is 1 for BPRMF on both datasets. Moreover, for BPRMF
in Movies∼Songs, learning rate=0.1∼1.346, bias regularization=0∼1.236, user
regularization=0.01∼1.575, positive item regularization=0.01∼1.376, and neg-
ative item regularization=0.01∼1.624; for SVDpp in Movies∼Songs, learning
rate=0.01∼0.001, factors regularization=0.1∼0.001, and bias regularization=0.001
in both datasets; NeuMF in Movies∼Songs, the multi-layer perceptron=10 in
both, learning rate=0.0025 in both, and factors regularization=0.1∼0.001.

6.2 Assessment of Disparities and Mitigation

Table 1 compares MOReGIn with the baselines in terms of the overall disparate
visibility, ∆T otal, for each continent. It is computed as ∀c ∈ C, ∆T otal =
(cid:80) ∆Vc. MOReGIn almost entirely reduces the disparities in both movies and
song datasets, where most results are ∆T otal = 0.0000. Although there is a
little difference in the ∆T otal between some approaches, these differences are
more explicit, considering the provider provenance. For example, in the movie
domain with the BPRMF algorithm, the ∆T otal value in the OR approach is
similar to that of PF. However, in a more detailed analysis of more representative
continents such as NA and EU, there are notorious differences between the two
approaches (i.e., 0.0075 for OR in contrast to -0.0066 for PF in the NA continent,
see the example shown in Figure 2a). It is important to highlight that in both
domains, our proposal mitigates the disparity regardless of the provenance of
the provider, in contrast to the other algorithms that show a clear dependence
on the data (i.e., the continent attribute).

Regarding the item genres, Table 2 compares MOReGIn with the baselines
in terms of the overall miscalibration, ∆Genre, for each continent. It is computed
as ∀g ∈ G and each user u ∈ U , ∆Genre = (cid:80) ∆Mug. For both datasets,
MOReGIn obtained the best ∆Genre (i.e., lowest miscalibration) in all the
recommendation models. An analysis of how the algorithms behave with the
different genres is shown in Fig. 2b. Although miscalibration never reaches values
of ∆Genre equal to zero, our proposal always calibrates better than the baselines.

12

G´omez et al.

(a) Movies ∆Vc

(b) Movies ∆Mug

Fig. 2: Disparity mitigation per continent (a) and miscalibration per genre
(b) in BPRMF.

Table 1: Results of disparity mitigation of continents in the Movies and
Songs datasets. Each value represents the sum of disparities, ∆T otal.

MOVIES

SONGS

OR CL PF MOReGIn OR CL PF MOReGIn

BPRMF 0.0539 0.0485 0.0576
0.1154 0.1085 0.1059
SVDpp
0.0395 0.0421 0.0638
NeuMF
UserKNN 0.0345 0.0327 0.0328
ItemKNN 0.0431 0.0418 0.0412

0.0000
0.0000
0.0000
0.0000
0.0000

0.2637 0.0840 0.2628
0.2678 0.1063 0.2445
0.4434 0.4516 0.3990
0.0361 0.0575 0.0370
0.0392 0.0583 0.0420

0.0000
0.0000
0.0000
0.0000
0.0000

Observation 2. MOReGIn, by taking action on the distribution of the
items per genre at the user level and provider provenance at the same time,
can both calibrate and be fair to the providers. This joint effort allows us to
improve the capability to calibrate the results and to be fair to providers with
respect to baselines devoted solely to these purposes.

6.3 Impact on the Quality of Recommendations

We evaluate the accuracy for the different approaches via the NDCG metric.

Table 3 shows its values for MOReGIn and the rest of the baselines, in all
the recommendation algorithms, for Movies and Songs. MOReGIn obtained a
better NDCG than the PF model, except for BPRMF and ItemKNN in the
Movies dataset, and UserKNN and ItemKNN in the Songs dataset. Similar re-
sults are obtained with the CL method. Comparing MOReGIn to a non-fair ap-
proach, MOReGIn outperforms OR models, with the exception of BPRMF and
ItemKNN in the Movie domain. Except for UserKNN and ItemKNN, MORe-
GIn also outperforms the OR model in the Songs domain.

All recommendation quality results show that the need for fairer and cali-
brated recommendations impacts the recommendation quality. However, beyond-
accuracy perspectives, such as those offered by MOReGIn allows for compen-
sating for the minimal loss in quality with more unbiased recommendations.

MOReGIn: Multi-Objective Recommendation

13

Table 2: Results of miscalibration of genres in the Movies and Songs
datasets. Each value represents the sum of miscalibrations, ∆Genre.

MOVIES

SONGS

OR CL PF MOReGIn OR CL PF MOReGIn

BPRMF 0.2892 0.2606 0.2454
0.5792 0.5026 0.5694
SVDpp
NeuMF
0.4596 0.3962 0.3735
UserKNN 0.0743 0.0862 0.0580
ItemKNN 0.2102 0.1966 0.1954

0.0634
0.1184
0.2901
0.0392
0.0559

5.5107 0.0772 0.4610
0.5773 0.1031 0.5029
1.2886 0.7494 1.2202
0.0298 0.0989 0.0291
0.0890 0.0601 0.0879

0.0289
0.0256
0.0787
0.0208
0.0205

Table 3: NDCG for each approach and recommendation algorithm.

MOVIES

SONGS

OR CL PF MOReGIn OR

PF MOReGIn

BPRMF 0.3204 0.3144 0.3195
0.0830 0.0888 0.0812
SVDpp
NeuMF
0.1963 0.1931 0.1956
UserKNN 0.3051 0.2954 0.3030
ItemKNN 0.3229 0.3145 0.3211

0.3057
0.1024
0.2050
0.3053
0.3131

CL
0.0034 0.0067 0.0031
0.0050 0.0103 0.0051
0.0183 0.0098 0.0179
0.3760 0.1925 0.3759
0.3860 0.1668 0.3857

0.0055
0.0138
0.0314
0.2648
0.2864

7 Conclusions and Future Work

Global and individual objectives in MORs have never been studied jointly.
To study this problem, we provided data, by i) extending the MovieLens-1M
dataset and ii) collecting a new dataset for song recommendation. The analysis
of this data showed that when users rate items of a given genre, the geographic
provenance of that item matters. Based on these insights, we proposed a new
post-processing approach, named MOReGIn, that aggregates the recommended
items into buckets, pairing item genres and their continent of production. Re-
sults show that MOReGIn outperforms the existing approaches at producing
effective, calibrated, and provider-fair recommendations. Future work will ex-
plore different strategies to generate recommendation lists given the generated
buckets. Moreover, we will consider consumer fairness as a global perspective.

Acknowledgments

D. Contreras research was partially funded by postdoctoral project (grant No. 74200094)
from ANID-Chile and by the supercomputing infrastructure of the NLHPC (ECM-
02). M. Salam´o was supported by the FairTransNLP-Language Project (MCIN-AEI-
10.13039-501100011033-FEDER) and by the Generalitat de Catalunya (2021 SGR
00313). Maria also belongs to the Associated unit to CSIC by IIIA.

14

G´omez et al.

References

1. Abdollahpouri, H., Mansoury, M., Burke, R., Mobasher, B.: The connection be-
tween popularity bias, calibration, and fairness in recommendation. In: Fourteenth
ACM conference on recommender systems. pp. 726–731 (2020)

2. Abdollahpouri, H., Mansoury, M., Burke, R., Mobasher, B., Malthouse, E.: User-
centered evaluation of popularity bias in recommender systems. In: Proceedings of
the 29th ACM Conference on User Modeling, Adaptation and Personalization. pp.
119–129 (2021)

3. Anelli, V.W., Bellogin, A., Ferrara, A., Malitesta, D., Merra, F.A., Pomo, C.,
Donini, F.M., Di Noia, T.: Elliot: A Comprehensive and Rigorous Framework for
Reproducible Recommender Systems Evaluation, p. 2405–2414. Association for
Computing Machinery, New York, NY, USA (2021)

4. Bellog´ın, A., Castells, P., Cantador, I.: Statistical biases in information retrieval
metrics for recommender systems. Inf. Retr. Journal 20(6), 606–634 (2017). https:
//doi.org/https://doi.org/10.1007/s10791-017-9312-z

5. Biega, A.J., Gummadi, K.P., Weikum, G.: Equity of attention: Amortizing indi-
vidual fairness in rankings. In: The 41st International ACM SIGIR Conference
on Research & Development in Information Retrieval, SIGIR 2018. pp. 405–414.
ACM, New York, NY, USA (2018). https://doi.org/10.1145/3209978.3210063
6. Chen, J., Wu, W., Shi, L., Zheng, W., He, L.: Long-tail session-based recommen-
dation from calibration. Appl. Intell. 53(4), 4685–4702 (2023). https://doi.org/
10.1007/s10489-022-03718-7, https://doi.org/10.1007/s10489-022-03718-7
7. Dokoupil, P., Peska, L., Boratto, L.: Looks can be deceiving: Linking user-
item interactions and user’s propensity towards multi-objective recommendations.
CoRR abs/2307.00654 (2023). https://doi.org/10.48550/arXiv.2307.00654,
https://doi.org/10.48550/arXiv.2307.00654

8. Dokoupil, P., Peska, L., Boratto, L.: Rows or columns? minimizing presenta-
tion bias when comparing multiple recommender systems. In: Chen, H., Duh,
W.E., Huang, H., Kato, M.P., Mothe, J., Poblete, B. (eds.) Proceedings of the
46th International ACM SIGIR Conference on Research and Development in In-
formation Retrieval, SIGIR 2023, Taipei, Taiwan, July 23-27, 2023. pp. 2354–
2358. ACM (2023). https://doi.org/10.1145/3539618.3592056, https://doi.
org/10.1145/3539618.3592056

9. Ekstrand, M.D., Das, A., Burke, R., Diaz, F.: Fairness in recommender systems. In:
Ricci, F., Rokach, L., Shapira, B. (eds.) Recommender Systems Handbook, pp. 679–
707. Springer US (2022). https://doi.org/10.1007/978-1-0716-2197-4\_18,
https://doi.org/10.1007/978-1-0716-2197-4_18

10. Ekstrand, M.D., Kluver, D.: Exploring author gender in book rating and rec-
ommendation. User Modeling and User-Adapted Interaction 31(3), 377–420
(2021). https://doi.org/10.1007/s11257-020-09284-2, https://doi.org/10.
1007/s11257-020-09284-2

11. Ekstrand, M.D., Tian, M., Kazi, M.R.I., Mehrpouyan, H., Kluver, D.: Explor-
ing author gender in book rating and recommendation. In: Proceedings of the
12th ACM Conference on Recommender Systems, RecSys 2018. pp. 242–250. ACM
(2018). https://doi.org/10.1145/3240323.3240373

12. Elahi, M., Ge, M., Ricci, F., Massimo, D., Berkovsky, S.: Interactive food recom-
mendation for groups. In: 8th ACM Conference on Recommender Systems, RecSys
2014. CEUR-WS (2014)

MOReGIn: Multi-Objective Recommendation

15

13. Fabbri, F., Bonchi, F., Boratto, L., Castillo, C.: The effect of homophily on dis-
parate visibility of minorities in people recommender systems. In: Proceedings of
the Fourteenth International AAAI Conference on Web and Social Media, ICWSM
2020. pp. 165–175. AAAI Press, USA (2020), https://ojs.aaai.org/index.php/
ICWSM/issue/view/262

14. Ferraro, A., Serra, X., Bauer, C.: What is fair? exploring the artists’ perspective
on the fairness of music streaming platforms. In: Human-Computer Interaction
- INTERACT 2021 - 18th IFIP TC 13 International Conference, Proceedings,
Part II. Lecture Notes in Computer Science, vol. 12933, pp. 562–584. Springer
(2021). https://doi.org/10.1007/978-3-030-85616-8\_33, https://doi.org/
10.1007/978-3-030-85616-8_33

15. Ge, Y., Zhao, X., Yu, L., Paul, S., Hu, D., Hsieh, C., Zhang, Y.: Toward pareto
efficient fairness-utility trade-off in recommendation through reinforcement learn-
ing. In: Candan, K.S., Liu, H., Akoglu, L., Dong, X.L., Tang, J. (eds.) WSDM
’22: The Fifteenth ACM International Conference on Web Search and Data
Mining, Virtual Event / Tempe, AZ, USA, February 21 - 25, 2022. pp. 316–
324. ACM (2022). https://doi.org/10.1145/3488560.3498487, https://doi.
org/10.1145/3488560.3498487

16. Gharahighehi, A., Vens, C., Pliakos, K.: Fair multi-stakeholder news rec-
Information Processing &
ommender
Management 58(5), 102663 (2021). https://doi.org/https://doi.org/10.
1016/j.ipm.2021.102663, https://www.sciencedirect.com/science/article/
pii/S0306457321001515

system with hypergraph ranking.

17. G´omez, E., Boratto, L., Salam´o, M.: Provider fairness across continents in col-
laborative recommender systems. Inf. Process. Manag. 59(1), 102719 (2022).
https://doi.org/10.1016/j.ipm.2021.102719

18. G´omez, E., Zhang, C.S., Boratto, L., Salam´o, M., Ramos, G.: Enabling cross-
continent provider fairness in educational recommender systems. Future Gener.
Comput. Syst. 127, 435–447 (2022). https://doi.org/10.1016/j.future.2021.
08.025

19. He, X., Liao, L., Zhang, H., Nie, L., Hu, X., Chua, T.S.: Neural collaborative
filtering. In: Proceedings of the 26th international conference on world wide web.
pp. 173–182 (2017)

20. Herlocker, J.L., Konstan, J.A., Riedl, J.: An empirical analysis of design choices
in neighborhood-based collaborative filtering algorithms. Inf. Retr. 5(4), 287–310
(2002). https://doi.org/10.1023/A:1020443909834

21. Jannach, D.: Multi-objective recommendation: Overview and challenges. In: Ab-
dollahpouri, H., Sahebi, S., Elahi, M., Mansoury, M., Loni, B., Nazari, Z., Di-
makopoulou, M. (eds.) Proceedings of the 2nd Workshop on Multi-Objective
Recommender Systems co-located with 16th ACM Conference on Recommender
Systems (RecSys 2022), Seattle, WA, USA, 18th-23rd September 2022. CEUR
Workshop Proceedings, vol. 3268. CEUR-WS.org (2022), https://ceur-ws.org/
Vol-3268/paper1.pdf

22. Jugovac, M., Jannach, D., Lerche, L.: Efficient optimization of multiple recommen-
dation quality factors according to individual user tendencies. Expert Systems with
Applications 81, 321–331 (2017). https://doi.org/https://doi.org/10.1016/
j.eswa.2017.03.055, https://www.sciencedirect.com/science/article/pii/
S0957417417302075

23. Karakolis, E., Kokkinakos, P., Askounis, D.: Provider fairness for diversity
recommender systems. Applied Sciences

and coverage in multi-stakeholder

16

G´omez et al.

12(10) (2022). https://doi.org/10.3390/app12104984, https://www.mdpi.com/
2076-3417/12/10/4984

24. Koren, Y.: Factorization meets the neighborhood: a multifaceted collaborative
filtering model. In: Proceedings of the 14th ACM SIGKDD International Con-
ference on Knowledge Discovery and Data Mining. pp. 426–434. ACM (2008).
https://doi.org/10.1145/1401890.1401944

25. Li, R., Kahou, S., Schulz, H., Michalski, V., Charlin, L., Pal, C.: Towards deep
conversational recommendations. In: Proceedings of the 32nd International Con-
ference on Neural Information Processing Systems. p. 9748–9758. NIPS’18, Curran
Associates Inc., Red Hook, NY, USA (2018)

26. Li, Y., Chen, H., Fu, Z., Ge, Y., Zhang, Y.: User-oriented fairness in recommenda-
tion. In: Leskovec, J., Grobelnik, M., Najork, M., Tang, J., Zia, L. (eds.) WWW
’21: The Web Conference 2021, Virtual Event / Ljubljana, Slovenia, April 19-23,
2021. pp. 624–632. ACM / IW3C2 (2021). https://doi.org/10.1145/3442381.
3449866, https://doi.org/10.1145/3442381.3449866

27. Lin, K., Sonboli, N., Mobasher, B., Burke, R.: Calibration in collaborative filtering
recommender systems: a user-centered analysis. In: Proceedings of the 31st ACM
Conference on Hypertext and Social Media. pp. 197–206 (2020)

28. Lin, X., Chen, H., Pei, C., Sun, F., Xiao, X., Sun, H., Zhang, Y., Ou, W., Jiang, P.:
A pareto-efficient algorithm for multiple objective optimization in e-commerce rec-
ommendation. In: Bogers, T., Said, A., Brusilovsky, P., Tikk, D. (eds.) Proceedings
of the 13th ACM Conference on Recommender Systems, RecSys 2019, Copenhagen,
Denmark, September 16-20, 2019. pp. 20–28. ACM (2019). https://doi.org/10.
1145/3298689.3346998, https://doi.org/10.1145/3298689.3346998

29. Marras, M., Boratto, L., Ramos, G., Fenu, G.: Equality of learning opportu-
nity via individual fairness in personalized recommendations. International Jour-
nal of Artificial Intelligence in Education (2021). https://doi.org/10.1007/
s40593-021-00271-1, https://doi.org/10.1007/s40593-021-00271-1

30. Mehrotra, R., McInerney, J., Bouchard, H., Lalmas, M., Diaz, F.: Towards a fair
marketplace: Counterfactual evaluation of the trade-off between relevance, fairness
& satisfaction in recommendation systems. In: Proceedings of the 27th ACM In-
ternational Conference on Information and Knowledge Management, CIKM 2018.
pp. 2243–2251. ACM, New York, NY, USA (2018). https://doi.org/10.1145/
3269206.3272027

31. Melchiorre, A.B., Rekabsaz, N., Parada-Cabaleiro, E., Brandl, S., Lesota, O.,
Schedl, M.: Investigating gender fairness of recommendation algorithms in the mu-
sic domain. Inf. Process. Manage. 58(5) (sep 2021)

32. Naghiaei, M., Rahmani, H.A., Deldjoo, Y.: Cpfair: Personalized consumer and pro-
ducer fairness re-ranking for recommender systems. In: SIGIR ’22: The 45th Inter-
national ACM SIGIR Conference on Research and Development in Information Re-
trieval. pp. 770–779. ACM (2022). https://doi.org/10.1145/3477495.3531959,
https://doi.org/10.1145/3477495.3531959

33. Nixon, J., Dusenberry, M.W., Zhang, L., Jerfel, G., Tran, D.: Measuring
calibration in deep learning. In: IEEE Conference on Computer Vision and
Pattern Recognition Workshops, CVPR Workshops 2019, Long Beach, CA,
USA, June 16-20, 2019. pp. 38–41. Computer Vision Foundation / IEEE (2019),
http://openaccess.thecvf.com/content_CVPRW_2019/html/Uncertainty_and_
Robustness_in_Deep_Visual_Learning/Nixon_Measuring_Calibration_in_
Deep_Learning_CVPRW_2019_paper.html

MOReGIn: Multi-Objective Recommendation

17

34. Peska, L., Dokoupil, P.: Towards results-level proportionality for multi-objective
recommender systems. In: Amig´o, E., Castells, P., Gonzalo, J., Carterette, B.,
Culpepper, J.S., Kazai, G. (eds.) SIGIR ’22: The 45th International ACM SI-
GIR Conference on Research and Development in Information Retrieval, Madrid,
Spain, July 11 - 15, 2022. pp. 1963–1968. ACM (2022). https://doi.org/10.1145/
3477495.3531787, https://doi.org/10.1145/3477495.3531787

35. Raj, A., Ekstrand, M.D.: Measuring fairness in ranked results: An analytical
and empirical comparison. In: SIGIR ’22: The 45th International ACM SIGIR
Conference on Research and Development in Information Retrieval. pp. 726–736.
ACM, New York, NY, USA (2022). https://doi.org/10.1145/3477495.3532018,
https://doi.org/10.1145/3477495.3532018

36. Rendle, S., Freudenthaler, C., Gantner, Z., Schmidt-Thieme, L.: BPR: bayesian
personalized ranking from implicit feedback. In: UAI 2009, Proceedings of the
Twenty-Fifth Conference on Uncertainty in Artificial Intelligence. pp. 452–461.
AUAI Press (2009)

37. Ricci, F., Rokach, L., Shapira, B.: Recommender systems: Techniques, applica-
tions, and challenges. In: Ricci, F., Rokach, L., Shapira, B. (eds.) Recommender
Systems Handbook, pp. 1–35. Springer US (2022). https://doi.org/10.1007/
978-1-0716-2197-4\_1, https://doi.org/10.1007/978-1-0716-2197-4_1
38. Rojas, C., Contreras, D., Salam´o, M.: Analysis of biases in calibrated recommen-
dations. In: Advances in Bias and Fairness in Information Retrieval. pp. 91–103.
Springer International Publishing, Cham (2022)

39. Sarwar, B.M., Karypis, G., Konstan, J.A., Riedl, J.: Item-based collaborative fil-
tering recommendation algorithms. In: Proceedings of the Tenth International
World Wide Web Conference, WWW 10. pp. 285–295. ACM (2001). https:
//doi.org/10.1145/371920.372071

40. Seymen, S., Abdollahpouri, H., Malthouse, E.C.: A constrained optimization ap-
proach for calibrated recommendations. In: Fifteenth ACM Conference on Recom-
mender Systems. pp. 607–612 (2021)

41. Stamenkovic, D., Karatzoglou, A., Arapakis, I., Xin, X., Katevas, K.: Choosing the
best of both worlds: Diverse and novel recommendations through multi-objective
reinforcement learning. In: Candan, K.S., Liu, H., Akoglu, L., Dong, X.L., Tang,
J. (eds.) WSDM ’22: The Fifteenth ACM International Conference on Web Search
and Data Mining, Virtual Event / Tempe, AZ, USA, February 21 - 25, 2022.
pp. 957–965. ACM (2022). https://doi.org/10.1145/3488560.3498471, https:
//doi.org/10.1145/3488560.3498471

42. Steck, H.: Calibrated recommendations. In: Proceedings of the 12th ACM Confer-
ence on Recommender Systems. p. 154–162. RecSys ’18, Association for Comput-
ing Machinery, New York, NY, USA (2018). https://doi.org/10.1145/3240323.
3240372

43. Wang, Z., Meng, C., Ji, S., Li, T., Zheng, Y.: Food package suggestion system based
on multi-objective optimization: A case study on a real-world restaurant. Applied
Soft Computing 93, 106369 (2020). https://doi.org/https://doi.org/10.1016/
j.asoc.2020.106369, https://www.sciencedirect.com/science/article/pii/
S1568494620303094

44. Wu, H., Ma, C., Mitra, B., Diaz, F., Liu, X.: Multi-fr: A multi-objective optimiza-
tion framework for multi-stakeholder fairness-aware recommendation. In: Transac-
tions on Information Systems (TOIS). ACM (2022)

45. Wu, H., Mitra, B., Ma, C., Diaz, F., Liu, X.: Joint multisided exposure fairness for
recommendation. In: Proceedings of the 45th International ACM SIGIR Conference

18

G´omez et al.

on Research and Development in Information Retrieval. p. 703–714. SIGIR ’22,
Association for Computing Machinery, New York, NY, USA (2022). https://doi.
org/10.1145/3477495.3532007, https://doi.org/10.1145/3477495.3532007
46. Zadrozny, B., Elkan, C.: Obtaining calibrated probability estimates from decision

trees and naive bayesian classifiers. In: Icml. vol. 1, pp. 609–616. Citeseer (2001)

47. Zehlike, M., Bonchi, F., Castillo, C., Hajian, S., Megahed, M., Baeza-Yates, R.:
Fa*ir: A fair top-k ranking algorithm. In: Proceedings of the 2017 ACM on Con-
ference on Information and Knowledge Management, CIKM 2017. pp. 1569–1578.
ACM, New York, NY, USA (2017). https://doi.org/10.1145/3132847.3132938
48. Zehlike, M., Castillo, C.: Reducing disparate exposure in ranking: A learning
to rank approach. In: WWW ’20: The Web Conference 2020. pp. 2849–2855.
ACM / IW3C2, New York, NY, USA (2020). https://doi.org/10.1145/3366424.
3380048

49. Zheng, Y., Wang, D.X.: A survey of recommender systems with multi-objective
optimization. Neurocomputing 474, 141–153 (2022). https://doi.org/10.1016/
j.neucom.2021.11.041, https://doi.org/10.1016/j.neucom.2021.11.041

