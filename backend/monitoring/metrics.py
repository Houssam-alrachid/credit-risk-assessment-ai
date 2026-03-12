"""
Prometheus metrics for monitoring credit assessment workflow performance.

This module defines metrics for tracking:
- Workflow execution duration
- Individual node execution duration
- LLM token usage
- Error rates
"""

from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps
from typing import Callable, Any
import asyncio

# Workflow-level metrics
workflow_duration = Histogram(
    'workflow_duration_seconds',
    'Total duration of credit assessment workflow',
    buckets=(5, 10, 15, 20, 25, 30, 40, 50, 60)
)

workflow_total = Counter(
    'workflow_total',
    'Total number of workflow executions',
    ['status']  # success, error
)

workflow_active = Gauge(
    'workflow_active',
    'Number of currently active workflows'
)

# Node-level metrics
node_duration = Histogram(
    'node_duration_seconds',
    'Duration of individual workflow nodes',
    ['node_name'],
    buckets=(1, 2, 3, 4, 5, 7, 10, 15, 20)
)

node_total = Counter(
    'node_total',
    'Total number of node executions',
    ['node_name', 'status']
)

# LLM metrics
llm_tokens = Counter(
    'llm_tokens_total',
    'Total LLM tokens consumed',
    ['direction', 'agent']  # direction: input/output, agent: agent name
)

llm_calls = Counter(
    'llm_calls_total',
    'Total number of LLM API calls',
    ['agent', 'status']
)

llm_latency = Histogram(
    'llm_latency_seconds',
    'LLM API call latency',
    ['agent'],
    buckets=(0.5, 1, 2, 3, 4, 5, 7, 10)
)

# Error metrics
errors_total = Counter(
    'errors_total',
    'Total number of errors',
    ['error_type', 'component']
)


def track_workflow_duration(func: Callable) -> Callable:
    """Decorator to track workflow execution duration."""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        workflow_active.inc()
        start_time = time.time()
        status = 'success'
        
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            status = 'error'
            errors_total.labels(
                error_type=type(e).__name__,
                component='workflow'
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            workflow_duration.observe(duration)
            workflow_total.labels(status=status).inc()
            workflow_active.dec()
    
    return wrapper


def track_node_duration(node_name: str):
    """Decorator to track individual node execution duration."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            status = 'success'
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'error'
                errors_total.labels(
                    error_type=type(e).__name__,
                    component=node_name
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                node_duration.labels(node_name=node_name).observe(duration)
                node_total.labels(node_name=node_name, status=status).inc()
        
        return wrapper
    return decorator


def track_llm_call(agent_name: str):
    """Decorator to track LLM API calls."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            status = 'success'
            
            try:
                result = await func(*args, **kwargs)
                
                # Track token usage if available in result
                if hasattr(result, 'usage_metadata'):
                    usage = result.usage_metadata
                    if hasattr(usage, 'input_tokens'):
                        llm_tokens.labels(
                            direction='input',
                            agent=agent_name
                        ).inc(usage.input_tokens)
                    if hasattr(usage, 'output_tokens'):
                        llm_tokens.labels(
                            direction='output',
                            agent=agent_name
                        ).inc(usage.output_tokens)
                
                return result
            except Exception as e:
                status = 'error'
                raise
            finally:
                duration = time.time() - start_time
                llm_latency.labels(agent=agent_name).observe(duration)
                llm_calls.labels(agent=agent_name, status=status).inc()
        
        return wrapper
    return decorator


def record_tokens(agent_name: str, input_tokens: int, output_tokens: int):
    """Manually record token usage for an agent."""
    llm_tokens.labels(direction='input', agent=agent_name).inc(input_tokens)
    llm_tokens.labels(direction='output', agent=agent_name).inc(output_tokens)


def record_error(error_type: str, component: str):
    """Manually record an error."""
    errors_total.labels(error_type=error_type, component=component).inc()
