d1ct - a hybrid object/mapping
===

FEATURES
---
 - directly inherited from dict
 - accessible by attribute.   o.x == o['x'] 
 - This works also for all corner cases.
 - json.dumps json.loads
 - vars() works on it!
 - hashable! (should not yet trust on it, though)
 - autocomplete works even if the objects comes from a list
 - best of all, it works recursively. So all inner dicts will become d1cts too.
 
   
  ![d1ct screenshot](https://i.imgur.com/AKStFpo_d.webp?maxwidth=780&fidelity=grand)  
  


>  ehhh, no downsides?   
>>**oh hell yeah it got downsides**  
  
   the performance which is a magnitude slower (~6x) than builtin dict  
   to give you an impression of timeit results:
   
   **d1ct**
   -----
  0.26289230000111274  
  0.2543108999961987  
  0.25743720002355985  
  0.2560539000260178  
  0.2556736999831628  
  0.25478869999642484  
  0.2541010999993887  
  0.2552008999919053  
  0.2651131000020541  
  0.25846979999914765  
   
  **dict**
  -----
  0.04928750000544824  
  0.04902900001616217  
  0.049049399996874854  
  0.050644999981159344  
  0.0496991999971214  
  0.04940899999928661  
  0.0497540999785997  
  0.04959690000396222  
  0.04939249999006279  
  0.04959330000565387   
      

  **So... this implementation might have side effects which I did not notice, because of different use cases or whatever.**
   
 
 Usage / Testing 
 ----
   
    import d1ct
    
    d = d1ct({"a": 1, "b": {"b1": "c1"}}, kw1=1, kw2=2)
    d["z1"] = {}
    d.z1.update({"yyyy": 2323232})
    
    assert d.a == d['a'] == 1
    assert d.z1 == d['z1'] == {'yyyy': 2323232}
    assert d == {'a': 1, 'b': {'b1': 'c1'}, 'kw1': 1, 'kw2': 2, 'z1': {'yyyy': 2323232}}
    assert type(d.z1) is d1ct
    
    d.z1.update({"yyyy": 2323232})
    assert type(d.z1.yyyy) is int
    
    d.z1.update({"yyyy": {"xbb": [1, 2, 23]}})
    assert type(d.z1.yyyy) is d1ct
    
    import json
    json.dumps(d)
    
    d |= {'more_keys': {'really': 'yeah!'}}
    
    assert d == {'a': 1,'b': {'b1': 'c1'}, 'kw1': 1,'kw2': 2, 'z1': {'yyyy': {'xbb': [1, 2, 23] } },'more_keys': {'really': 'yeah!'} }

