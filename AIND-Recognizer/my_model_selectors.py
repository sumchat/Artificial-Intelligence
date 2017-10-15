import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        
        p in BIC is the number of free parameters, and N is the number of data points
        p in hmm model is the sum total of parameters in
        i)Initial propbability matrix which is n -1 as the sum total is 1 the last one can be calculated from others.
        ii)Transition probability matrix(n states) which is n *(n-1) as the last column can be calculated from others
        iii)Emission probability matrix :Observation for each feature in each state is characterised by a mean and variance.
        Variances are the size of the covars array, Since we are using "diag" so it will be n*d
        So no of free parameters are 2 * n * d where d is no of features and n is no of states.
        So p = n*(n-1) + (n-1) + 2*n*d = n *n + 2*n*d -1
        Lower the BIC value better the model
        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        
        BIC = float('inf')
        best_num_components = 0           
        for n in range(self.min_n_components, self.max_n_components + 1): 
                                                             
                    try:                            
                        hmm_model = GaussianHMM(n_components = n, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)                              
                                
                        logL = hmm_model.score(self.X, self.lengths)
                        no_freeParameters = n * n + 2 * n * self.X.shape[1] - 1
                        bic_value = -2 * logL + no_freeParameters * np.log(len(self.X))  
                                                                           
                        if BIC > bic_value:
                                BIC = bic_value
                                best_num_components = n
                            
                    except:                        
                        pass          
                   
        if  best_num_components != 0:           
             hmm_model = GaussianHMM(n_components = best_num_components, covariance_type="diag", n_iter=1000,        
                                 random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
        else:
            hmm_model = self.base_model(self.n_constant)
        return hmm_model
        


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    Unlike the Bayes Factor criterion, the Discriminant Factor Criterion is the difference between the evidence of the
    model, given the corresponding data set, and the average over anti-evidences of the model. The antievidence is computed
    by finding the score for all the rest of the words except the one for which the model is generated.
    By choosing the model which maximizes the evidence, and minimize the antievidences,the result is the 
    best generative model for the correct class and the worst generative model for the competitive classes;
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        
        DIC = float('-inf')
        best_num_components = 0           
        for n in range(self.min_n_components, self.max_n_components + 1): 
                                                             
                    try:                            
                        hmm_model = GaussianHMM(n_components = n, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)                              
                                
                        logL = hmm_model.score(self.X, self.lengths)
                        totalScore = 0
                        noWords = 0
                        for word in self.hwords:
                            if word != self.this_word:
                                X, lengths = self.hwords[word]
                                score = hmm_model.score(X, lengths)
                                totalScore += score
                                noWords +=1
                        averageScore = totalScore/len(self.hwords) - 1
                        dic_value =  logL - averageScore                        
                                                                            
                        if DIC < dic_value:
                                DIC = dic_value
                                best_num_components = n
                            
                    except:
                        #if self.verbose:
                        #    print("failure  with {} states".format(num_states))
                        pass 
        if  best_num_components != 0:           
             hmm_model = GaussianHMM(n_components = best_num_components, covariance_type="diag", n_iter=1000,        
                                 random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
        else:
            hmm_model = self.base_model(self.n_constant)
        return hmm_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        if len(self.sequences) < 2:
            hmm_model = GaussianHMM(n_components=3, covariance_type="diag", n_iter=1000,                                  random_state=self.random_state, verbose=self.verbose).fit(self.X, self.lengths)
            return hmm_model
        else:            
            kf = KFold(n_splits=min(3,len(self.sequences)))
            max_score = None
            best_num_components = None           
            for num_states in range(self.min_n_components, self.max_n_components + 1): 
                    total_logL = 0;
                    n=0   
                    for train_index, test_index in kf.split(self.sequences):    
                            
                            trainSequence, trainSequenceLengths = combine_sequences(train_index, self.sequences)
                            testSequence, testSequencelengths = combine_sequences(test_index, self.sequences)                   
                            try:                            
                                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,    random_state=self.random_state, verbose=self.verbose).fit(trainSequence, trainSequenceLengths)
                                score = hmm_model.score(testSequence, testSequencelengths)
                                total_logL += score
                                n +=1
                            except:
                                if self.verbose:
                                    print("failure  with {} states".format(num_states))
                                pass
                    if n != 0:        
                        avg_logL = total_logL/n                    
                    else:  
                        avg_logL = 0
                    
                        
                    if  max_score == None or max_score < avg_logL:
                                 max_score = avg_logL
                                 if max_score != 0:
                                    best_num_components = num_states
            
            if  best_num_components != None:           
                hmm_model = GaussianHMM(n_components = best_num_components, covariance_type="diag", n_iter=1000,        
                                 random_state=self.random_state, verbose=self.verbose).fit(self.X, self.lengths)
            else:
                hmm_model = self.base_model(self.n_constant)
            
            return hmm_model
        
