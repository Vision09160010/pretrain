import torch
from torch.fx.experimental.migrate_gradual_types.z3_types import dim


def bayes(p_b_given_a,p_a,p_b):
    """
    :param p_b_given_a: P(B|A)
    :param p_a: P(A)
    :param p_b: P(B)
    :return: p_a_given_b : P(A|B)
    """
    p_a_given_b = (p_b_given_a*p_a)/p_b
    return p_a_given_b



def bayes_multi(prior,likelihood):
    """
    :param prior:  P(A_i)
    :param likelihood: P(B|A_i)
    :return:
    """
    numerator = prior * likelihood
    evidence = torch.sum(numerator)
    posterior = numerator / evidence
    return posterior


def bayes_batch(prior,likelihood):
    """
    :param prior: (batch, n_class)
    :param likelihood: (batch, n_class)
    :return:
    """
    numerator = prior * likelihood
    evidence = numerator.sum(dim=1,keepdim=True)
    posterior = numerator / evidence
    return posterior


if __name__ == '__main__':
    p_b_given_a  =  torch.tensor(0.99)
    p_a = torch.tensor(0.01)
    p_b = torch.tensor(0.0594)
    result = bayes(p_b_given_a,p_a,p_b)
    print(result)
    print("-"*50)
    """
    -------------------------------------
    """
    prior = torch.tensor([0.2,0.5,0.3])
    likelihood = torch.tensor([0.8,0.6,0.1])
    posterior = bayes_multi(prior,likelihood)
    print(posterior)
    print("-"*50)

    prior = torch.tensor([
        [0.2, 0.5, 0.3],
        [0.3, 0.3, 0.4]
    ])

    likelihood = torch.tensor([
        [0.8, 0.6, 0.1],
        [0.5, 0.2, 0.7]
    ])

    posterior = bayes_batch(prior, likelihood)

    print(posterior)
    print("-" * 50)



def bayes_log(prior, likelihood):

    log_prior = torch.log(prior)
    log_likelihood = torch.log(likelihood)

    log_posterior = log_prior + log_likelihood

    posterior = torch.softmax(log_posterior, dim=-1)

    return posterior